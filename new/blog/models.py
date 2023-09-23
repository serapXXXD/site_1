from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(verbose_name='Слаг')
    title = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Post(models.Model):
    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='Автор поста')
    title = models.CharField(max_length=255, verbose_name='Название')
    photo = models.ImageField(
        upload_to='photos', verbose_name='Фото', blank=True, null=True)
    body = models.TextField(verbose_name='Текст поста')
    tags = models.ManyToManyField('Tag', verbose_name='Тэги')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата изменения')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Запись в блоге'
        verbose_name_plural = 'Записи в блоге'
        ordering = ['-id']


class Tag(models.Model):
    slug = models.SlugField(verbose_name='Слаг')
    title = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             verbose_name='Публикация', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор комментария', related_name='comments')
    text = models.TextField(max_length=1500, verbose_name='Текст комментария')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата изменения')
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Ответ на', null=True, blank=True, related_name='replies')

    def __str__(self) -> str:
        return f"{self.post.title}: {self.text[:100]}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
