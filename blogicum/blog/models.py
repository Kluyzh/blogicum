from django.contrib.auth import get_user_model
from django.db import models

from .constants import LENGTH_OF_SELF_NAME, MAX_LENGTH
from .queryset import PostQuerySet

User = get_user_model()


class CreationTime(models.Model):
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Publish(CreationTime):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta(CreationTime.Meta):
        abstract = True


class Category(Publish):
    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta(Publish.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        ending = ''
        if LENGTH_OF_SELF_NAME < len(self.title):
            ending = '...'
        return self.title[:LENGTH_OF_SELF_NAME] + ending


class Location(Publish):
    name = models.CharField('Название места', max_length=MAX_LENGTH)

    class Meta(Publish.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        ending = ''
        if LENGTH_OF_SELF_NAME < len(self.name):
            ending = '...'
        return self.name[:LENGTH_OF_SELF_NAME] + ending


class Post(Publish):
    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    objects = PostQuerySet.as_manager()

    class Meta(Publish.Meta):
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        ending = ''
        if LENGTH_OF_SELF_NAME < len(self.title):
            ending = '...'
        return self.title[:LENGTH_OF_SELF_NAME] + ending


class Comment(CreationTime):
    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta(CreationTime.Meta):
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
