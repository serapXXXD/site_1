from django.db import models
from blog.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True, upload_to='user_photos', verbose_name='Аватар')


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
    # кто лайкает
    liker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    # какой пост лайкают
    liked_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'
        ordering = ['-id']
        constraints = [models.UniqueConstraint(
            fields=['liker', 'liked_post'], name='unique_together_liker_post')]
