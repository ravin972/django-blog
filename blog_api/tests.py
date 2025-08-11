# blog_api/tests.py
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post

class PostViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.other_user = User.objects.create_user(username="otheruser", password="pass123")

        self.public_post = Post.objects.create(
            title="Public Post",
            content="This is public.",
            is_private=False,
            author=self.other_user
        )

        self.private_post = Post.objects.create(
            title="Private Post",
            content="This is private.",
            is_private=True,
            author=self.other_user
        )

        self.api_url = "/api/posts/"

    def test_list_posts_as_anonymous(self):
        """Anonymous users should only see public posts"""
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_posts_as_authenticated(self):
        """Authenticated users see public posts + their own private posts"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post_authenticated(self):
        """Authenticated users can create posts"""
        self.client.force_authenticate(user=self.user)
        data = {"title": "New Post", "content": "Test content", "is_private": False}
        response = self.client.post(self.api_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(Post.objects.last().author, self.user)

    def test_create_post_anonymous(self):
        """Anonymous users cannot create posts"""
        data = {"title": "Anon Post", "content": "Test content", "is_private": False}
        response = self.client.post(self.api_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_post(self):
        """Anyone can retrieve a public post"""
        url = f"{self.api_url}{self.public_post.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Public Post")

    def test_update_post_by_owner(self):
        """Only the post owner can update their post"""
        self.client.force_authenticate(user=self.user)
        my_post = Post.objects.create(title="Mine", content="Body", author=self.user)
        url = f"{self.api_url}{my_post.id}/"
        response = self.client.put(url, {"title": "Updated", "content": "New Body", "is_private": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=my_post.id).title, "Updated")

    def test_update_post_by_non_owner(self):
        """Non-owners cannot update posts of others"""
        self.client.force_authenticate(user=self.user)
        url = f"{self.api_url}{self.public_post.id}/"
        response = self.client.put(url, {"title": "Hack", "content": "New", "is_private": False})
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
