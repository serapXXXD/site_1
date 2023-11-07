from django.contrib.auth import get_user_model
from core.tests.base_test import BaseTest
from authentication.models import Like, Subscription
from django.db.utils import IntegrityError

User = get_user_model()


class TesAPIModels(BaseTest):

    def test_like_unique_together(self):
        like_1 = Like.objects.create(liker=self.test_user_1, liked_post=self.test_post)
        try:
            like_2 = Like.objects.create(liker=self.test_user_1, liked_post=self.test_post)
            is_error = False
        except IntegrityError as er:
            is_error = True
        self.assertTrue(is_error)

    def test_subscription_unique_together(self):
        subscribe_1 = Subscription.objects.create(subscriber=self.test_user_1, author=self.test_post.author)
        try:
            subscribe_2 = Subscription.objects.create(subscriber=self.test_user_1, author=self.test_post.author)
            is_error = False
        except IntegrityError as er:
            is_error = True
        self.assertTrue(is_error)
