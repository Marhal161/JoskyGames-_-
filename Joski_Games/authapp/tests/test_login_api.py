import pytest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import User

@pytest.mark.django_db
class TestLoginView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('login')  # Убедитесь, что у вас есть соответствующий URL-маршрут
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_successful_login(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'access_token' in response.cookies
        assert 'refresh_token' in response.cookies
        assert response.data['user_id'] == self.user.id

    def test_invalid_password_login(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == {'non_field_errors': [ErrorDetail(string='Неверный логин или пароль', code='invalid')]}

    def test_invalid_email_login(self):
        data = {
            'email': 'wrongemail@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == {'non_field_errors': [ErrorDetail(string='Неверный логин или пароль', code='invalid')]}

    def test_missing_fields_login(self):
        data = {
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_invalid_email_format_login(self):
        data = {
            'email': 'invalidemail',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data