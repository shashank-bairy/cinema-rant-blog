from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import get_unique_slug
from PIL import Image

DEFAULT_CATEGORY_ID = 1
DEFAULT_POST_ID = 1
DEFAULT_COMMENT_ID = 1


# Category model definition
class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    slug = models.SlugField(max_length=70,
                            unique=True,
                            null=True,
                            blank=True,
                            editable=False)

    def get_absolute_url(self):
        # return path to post-detail route with specific primary key
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)


# Post model definition
class Post(models.Model):
    title = models.CharField(max_length=120, verbose_name='Title')
    slug = models.SlugField(max_length=140,
                            unique=True,
                            null=True,
                            blank=True,
                            editable=False)
    thumbnail_img = models.ImageField(default='default.jpeg',
                                      upload_to='thumbnail/')
    category = models.ForeignKey(Category,
                                 default=DEFAULT_CATEGORY_ID,
                                 verbose_name='Category',
                                 on_delete=models.CASCADE)
    content = RichTextUploadingField(blank=False,
                                     null=False,
                                     verbose_name='Post content')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True,
                                      null=True,
                                      verbose_name='Created at',
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True,
                                      verbose_name='Updated at',
                                      editable=False)

    # like_count = models.BigIntegerField(default=0,
    #                                     verbose_name='Number of likes',
    #                                     editable=False)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return path to post-detail route with specific primary key
        return reverse('post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)
        # to resize thumbnail
        img = Image.open(self.thumbnail_img.path)
        if img.height > 450 or img.width > 800:
            output_size = (450, 800)
            img.thumbnail(output_size)
            img.save(self.thumbnail_img.path)


# Like model definition
class Like(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             default=DEFAULT_POST_ID,
                             verbose_name='Post')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Liked by')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f'Liked by {self.user.username}'


# Comment model definition
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             default=DEFAULT_POST_ID,
                             verbose_name='Post')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Author')
    content = models.TextField(blank=False,
                               null=False,
                               verbose_name='Comment content')
    created_at = models.DateTimeField(auto_now_add=True,
                                      null=True,
                                      verbose_name='Created at',
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True,
                                      verbose_name='Updated at',
                                      editable=False)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username}'
