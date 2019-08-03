from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import get_unique_slug
from django.dispatch import receiver
from PIL import Image
import os

DEFAULT_CATEGORY_ID = 1
DEFAULT_POST_ID = 1
DEFAULT_COMMENT_ID = 1


# Category (Movies, TV shows,etc) model definition
class Category(models.Model):
    # category title
    title = models.CharField(max_length=50, verbose_name='Title')
    # slug for the title
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
        # generate slug for category title
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)


# Post model definition
class Post(models.Model):
    # post title
    title = models.CharField(max_length=120, verbose_name='Title')
    # unique slug for the post to be used in URL as parameter
    slug = models.SlugField(max_length=140,
                            unique=True,
                            null=True,
                            blank=True,
                            editable=False)
    # thumbnail image for the post (if necessary)
    thumbnail_img = models.ImageField(default='default.jpeg',
                                      upload_to='thumbnail/')
    # category to which the post belongs
    category = models.ForeignKey(Category,
                                 default=DEFAULT_CATEGORY_ID,
                                 verbose_name='Category',
                                 on_delete=models.CASCADE)
    # post content (Uses Ckeditor field)
    content = RichTextUploadingField(blank=False,
                                     null=False,
                                     verbose_name='Post content')
    # author of the post
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Author')
    # post creation time
    created_at = models.DateTimeField(auto_now_add=True,
                                      null=True,
                                      verbose_name='Created at',
                                      editable=False)
    # last updated time 
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True,
                                      verbose_name='Updated at',
                                      editable=False)
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
        # Get unique slug for the post 
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')

        super().save(*args, **kwargs)

        # to resize image thumbnail
        img = Image.open(self.thumbnail_img.path)
        if img.height > 450 or img.width > 800:
            output_size = (450, 800)
            img.thumbnail(output_size)
            img.save(self.thumbnail_img.path)

# Delete the post thumbnail image on deleting the UserProfile object
@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes thumbnail_img from filesystem
    when corresponding `Post` object is deleted.
    """
    # and 'default.jpeg' not in old_image.path
    if instance.thumbnail_img:
        if os.path.isfile(instance.thumbnail_img.path
                          ) and 'default.jpeg' not in instance.thumbnail_img.path:
            os.remove(instance.thumbnail_img.path)

# Delete the old thumbnail image on changing the post thumbnail image
@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old thumbnail_img from filesystem
    when corresponding `Post` object is updated
    with new thumbnail_img.
    """
    if not instance.pk:
        return False

    try:
        old_thumbnail_img = sender.objects.get(pk=instance.pk).thumbnail_img
    except sender.DoesNotExist:
        return False

    new_thumbnail_img = instance.thumbnail_img
    if not old_thumbnail_img == new_thumbnail_img:
        if os.path.isfile(
                old_thumbnail_img.path) and 'default.jpeg' not in old_thumbnail_img.path:
            os.remove(old_thumbnail_img.path)


# Like model definition
# class Like(models.Model):
#     post = models.ForeignKey(Post,
#                              on_delete=models.CASCADE,
#                              default=DEFAULT_POST_ID,
#                              verbose_name='Post')
#     user = models.ForeignKey(User,
#                              on_delete=models.CASCADE,
#                              verbose_name='Liked by')

#     class Meta:
#         verbose_name = 'Like'
#         verbose_name_plural = 'Likes'

#     def __str__(self):
#         return f'Liked by {self.user.username}'