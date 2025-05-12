from email.policy import default
from django.urls import reverse
from django.db import models
from django.template.base import kwarg_re
from django.template.defaultfilters import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'


    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    photo = models.FileField(upload_to='photos/%Y/%m/%d', default=None, blank=True, null=True,
                             verbose_name='Фото')
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
    class Mete:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag
    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_media')
