# blog/tets/test_permisions.py

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from blog.models import BlogPost
from rest_framework import status

@pytest.mark.django_db
class TestIsAuthenticatedOrReadOnly:
    def setup_method(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass')
        self.authenticated_user = User.objects.create_user(username='user', password='userpass')
        self.blog_post = BlogPost.objects.create(titulo='Test Post', contenido='Test Content')

    def test_authenticated_user_allowed(self):
        self.client.force_authenticate(user=self.authenticated_user)
        response = self.client.get(f'/api/blogpost/{self.blog_post.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_denied(self):
        response = self.client.delete(f'/api/blogpost/{self.blog_post.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_superuser_allowed_all_methods(self):
        self.client.force_authenticate(user=self.superuser)
        
        # Test GET
        response = self.client.get(f'/api/blogpost/{self.blog_post.id}/')
        assert response.status_code == status.HTTP_200_OK
        
        # Test POST
        response = self.client.post('/api/blogpost/', {'titulo': 'New Post', 'contenido': 'New Content'})
        assert response.status_code == status.HTTP_201_CREATED
        
        # Test PUT
        response = self.client.put(f'/api/blogpost/{self.blog_post.id}/', {'titulo': 'Updated Post', 'contenido': 'Updated Content'})
        assert response.status_code == status.HTTP_200_OK

        # Test POST comment
        response = self.client.post(f'/api/blogpost/{self.blog_post.id}/comentarios/', {'autor': 'joel', 'contenido': 'Great post!'})
        assert response.status_code == status.HTTP_201_CREATED

        # Test GET comments
        response = self.client.get(f'/api/blogpost/{self.blog_post.id}/comentarios/')
        assert response.status_code == status.HTTP_200_OK
        
        # Test DELETE
        response = self.client.delete(f'/api/blogpost/{self.blog_post.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_authenticated_user_denied_non_get_methods(self):
        self.client.force_authenticate(user=self.authenticated_user)

        # Test GET list
        response = self.client.get('/api/blogpost/')
        assert response.status_code == status.HTTP_200_OK

        # Test GET 1
        response = self.client.get(f'/api/blogpost/{self.blog_post.id}/')
        assert response.status_code == status.HTTP_200_OK
        
        # Test POST
        response = self.client.post('/api/blogpost/', {'titulo': 'New Post', 'contenido': 'New Content'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Test PUT
        response = self.client.put(f'/api/blogpost/{self.blog_post.id}/', {'titulo': 'Updated Post', 'contenido': 'Updated Content'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Test POST comment
        response = self.client.post(f'/api/blogpost/{self.blog_post.id}/comentarios/', {'autor': 'joel', 'contenido': 'Great post!'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Test GET comments
        response = self.client.get(f'/api/blogpost/{self.blog_post.id}/comentarios/')
        assert response.status_code == status.HTTP_200_OK

        # Test DELETE
        response = self.client.delete(f'/api/blogpost/{self.blog_post.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

