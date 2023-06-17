from django.db import models
from blog.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()


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
                fields=['subscriber', 'author'], name='unuque_together_subscriber_author'),
        ]


class Like(models.Model):
    # кто лайкает
    liker = models.ManyToManyField(User)
    # какой пост лайкают
    liked_post = models.ManyToManyField(Post)
    # я думаю что вроде как больше полей то и не нужно

    class Meta:
        verboe_name = 'лайк'
        verboe_name_plular = 'лайки'
        ordering = ['-id']
        constraints = [models.UniqueConstraint(
            fields=['liker', 'liked_post'], name='unique_together_liker_post')]
