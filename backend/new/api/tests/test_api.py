from django.contrib.auth import get_user_model
from blog.models import Post
from core.tests.base_test import BaseTest
from rest_framework import status

User = get_user_model()


class TesAPIViews(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.like_count = cls.test_post.likes.count
        cls.url_user2 = f'/api/v1/users/{cls.test_user_2.id}/'
        cls.url_post = f'/api/v1/posts/{cls.test_post.id}/'
        cls.like_url = url = f'/api/v1/posts/{cls.test_post.id}/like/'

    def test_like(self):
        likes_before = self.like_count()
        print(likes_before)
        resp = self.test_user_2_api_client.post(self.like_url)
        likes_after = self.like_count()
        print(likes_after)
        self.assertTrue(likes_after > likes_before)

    def test_like_cancel(self):
        likes_before = self.like_count()
        resp_put_like = self.test_user_1_api_client.post(self.like_url)
        self.assertEquals(resp_put_like.status_code, status.HTTP_201_CREATED)
        resp_cancel_like = self.test_user_1_api_client.post(self.like_url)
        self.assertEquals(resp_cancel_like.status_code, status.HTTP_200_OK)
        likes_after = self.like_count()
        self.assertEquals(likes_before, likes_after)

    def test_like_unauthorized_user(self):
        resp = self.unauthorized_api_client.post(self.like_url)
        self.assertEquals(resp.status_code, 401)
        self.assertEquals(self.like_count(), 0)

    def test_get_users(self):
        resp = self.test_user_1_api_client.get(self.url_user2)
        self.assertEquals(resp.status_code, 200)

    def test_get_users_for_unauthorized_user(self):
        resp = self.unauthorized_api_client.get(self.url_user2)
        self.assertEquals(resp.status_code, 401)

    def test_get_posts(self):
        resp = self.test_user_1_api_client.get(self.url_post)
        self.assertEquals(resp.status_code, 200)

    def test_404_post(self):
        last_post_id = Post.objects.order_by('id').last().id
        resp = self.unauthorized_api_client.get(f'/api/v1/posts/{last_post_id + 1}/')
        self.assertEquals(resp.status_code, 404)

