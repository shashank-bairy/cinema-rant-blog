from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
import os

# User Profile Model
class UserProfile(models.Model):
    # user to which the profile belongs
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # unique identifier used to naviagte via URL
    slug = models.SlugField(max_length=50,
                            unique=True,
                            null=True,
                            blank=True,
                            editable=False)
    # profile image of user
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    # date of birth of user
    dob = models.DateField(blank=False, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('user-profile-detail', kwargs={'slug': self.slug})

    @property
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        
        super().save(*args, **kwargs)

        # Resize the image to size 300 x 300 before saving
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# Create user profile on creating a new user and link to it
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Save user profile on creating user
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# Delete the profile image on deleting the UserProfile object
@receiver(models.signals.post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `UserProfile` object is deleted.
    """
    # and 'default.jpeg' not in old_image.path
    if instance.image:
        if os.path.isfile(instance.image.path
                          ) and 'default.jpeg' not in instance.image.path:
            os.remove(instance.image.path)

# Delete the old profile image on changing the profile image
@receiver(models.signals.pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old image from filesystem
    when corresponding `UserProfile` object is updated
    with new image.
    """
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(
                old_image.path) and 'default.jpeg' not in old_image.path:
            os.remove(old_image.path)