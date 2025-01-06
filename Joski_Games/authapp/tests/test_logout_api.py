import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User

@pytest.mark.django_db
class TestLogoutView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('logout')  # Убедитесь, что у вас есть соответствующий URL-маршрут
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.refresh_token = RefreshToken.for_user(self.user)

    def test_successful_logout(self):
        self.client.cookies['refresh_token'] = str(self.refresh_token)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['message'] == 'Вы успешно вышли из системы.'
        assert 'access_token' not in response.cookies
        assert 'refresh_token' not in response.cookies

    def test_no_active_session_logout(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False
        assert response.data['message'] == 'Нет активного сеанса.'

    def test_invalid_refresh_token_logout(self):
        self.client.cookies['refresh_token'] = 'invalid_token'
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False
        assert 'Ошибка при выходе из системы' in response.data['message']

    def test_exception_handling_logout(self):
        # Симуляция исключения
        def mock_get_jti(self):
            raise Exception('Test exception')

        # Патчим метод set_jti для симуляции исключения
        from unittest.mock import patch
        with patch('rest_framework_simplejwt.tokens.RefreshToken.set_jti', mock_get_jti):
            self.client.cookies['refresh_token'] = str(self.refresh_token)
            response = self.client.get(self.url)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.data['success'] is False
            assert 'Ошибка при выходе из системы' in response.data['message']