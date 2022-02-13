from django.db import models
from random import randint
from django.contrib.auth.models import User
from datetime import datetime

current_time = datetime.now()
# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=64)
    avatar = models.ImageField(upload_to="author", blank=True)
 
    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=100)
    script = models.CharField(max_length=200, blank=True)
    category_image = models.ImageField(upload_to="dashboard", blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class News(models.Model):
    headlines = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to="news", blank=True, null=True)
    image_square = models.ImageField(upload_to="news square", blank=True, null=True)
    article = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_news")
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, default='Crypto', related_name="category_news")
    add_time = models.DateTimeField()
    tag = models.ManyToManyField(Tag, blank=True, related_name="newsTag")
    views = models.PositiveIntegerField(default=randint(0,50))
    cmt_count = models.PositiveIntegerField(default=randint(0,5))

    class Meta:
        ordering = ['-views','-add_time']
        verbose_name_plural = "News"

    def tag_titles(self):
        return ', '.join([a.title for a in self.tag.all()])
    tag_titles.short_description = "tag titles"

    def __str__(self):
        return f"{self.headlines}"


class Comment(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=200)
    comment = models.TextField()
    cmt_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    news = models.ForeignKey(News, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='post_comments')
    avatar = models.ImageField(upload_to="user_ava", blank=True, null=True)

    def __str__(self):
        return f"{self.name}: {self.email}"
