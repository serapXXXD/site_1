from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from blog.models import Post, Category, Tag

User = get_user_model()


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user_1 = User.objects.create_user(username='user99', email='3bngnbdjn@mail.com', password='Qq123456')
        cls.test_user_1.save()
        cls.test_user_2 = User.objects.create_user(username='user100',email='4bngnbdjn@mail.com', password='Qq123456')
        cls.test_user_2.save()
        cls.test_category = Category.objects.create(slug='test_cat', title='test_cat')
        cls.test_post = Post.objects.create(author=cls.test_user_1, title='123', body='321', category=cls.test_category)
        cls.test_tag = Tag.objects.create(slug='test_tag_slug', title='tes_tag')
        cls.unauthorized_api_client = APIClient()
        cls.test_user_1_api_client = APIClient()
        cls.test_user_1_api_client.force_authenticate(cls.test_user_1)
        cls.test_user_2_api_client = APIClient()
        cls.test_user_2_api_client.force_authenticate(cls.test_user_2)
