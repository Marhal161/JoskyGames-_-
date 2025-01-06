import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import User

@pytest.mark.django_db
class TestRegisterView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('register')  # Убедитесь, что у вас есть соответствующий URL-маршрут

    def test_successful_registration(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert 'access_token' in response.cookies
        assert 'refresh_token' in response.cookies
        assert User.objects.filter(username='testuser').exists()

    def test_duplicate_email_registration(self):
        User.objects.create(username='testuser1', email='testuser@example.com', password='testpassword')
        data = {
            'username': 'testuser2',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_duplicate_username_registration(self):
        User.objects.create(username='testuser', email='testuser1@example.com', password='testpassword')
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser2@example.com',
            'password': 'testpassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data

    def test_invalid_data_registration(self):
        data = {
            'username': '',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalidemail',
            'password': 'testpassword',
            'phone': '1234567890'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
        assert 'email' in response.data

    def test_missing_fields_registration(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'phone': '1234567890'
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data
