from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Группа',
        help_text='Дайте название группе'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200
    )
    description = models.TextField(
        max_length=300
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    text = models.TextField(
        help_text='Напишите текст',
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        "date published",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ("-pub_date",)
