from django.db import models
from django.contrib.auth.models import User


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
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор поста', null=True )
    title = models.CharField(max_length=255, verbose_name='Название')
    body = models.TextField(verbose_name='Текст поста')
    photo = models.ImageField(upload_to='photos', null=True, blank=True, verbose_name='Фото')
    tags = models.ManyToManyField('Tag', verbose_name='Тэги')
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
'__all__'