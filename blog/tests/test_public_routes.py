import pytest
from blog.models import BlogPost 
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestPublicRoutes:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='userpass')
        self.blog_post = BlogPost.objects.create(
            titulo='Test Post', 
            contenido='Test Content',
            autor=self.user
            )

    def test_token_route_nonexistent_user(self):
        response = self.client.post('/api/token/', {'username': 'any', 'password': 'any'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_route_existing_user(self):
        response = self.client.post('/api/token/', {'username': 'user', 'password': 'userpass'})
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_admin_route_is_public(self):
        response = self.client.get('/admin/')
        assert response.status_code == status.HTTP_302_FOUND # Redirección a login
        assert '/admin/login/' in response.url 

    def test_blogpost_list_requires_authentication(self):
        response = self.client.get('/api/blogpost/')
        assert response.status_code == status.HTTP_200_OK