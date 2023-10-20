from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from allauth.socialaccount.models import SocialAccount


class User(AbstractUser):
    photo = models.ImageField(null=True, blank=True, upload_to='user_photos', verbose_name='Аватар')
    email = models.EmailField(unique=True, max_length=64)
    description = models.CharField(null=True, blank=True, max_length=255, verbose_name='О себе')

    def is_social_account(self):
        is_social = SocialAccount.objects.filter(user=self).exists()
        return is_social


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'], name='unique_together_subscriber_author'),
        ]


class Like(models.Model):
    liker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    liked_post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'
        ordering = ['-id']
        constraints = [models.UniqueConstraint(
            fields=['liker', 'liked_post'], name='unique_together_liker_post')]
