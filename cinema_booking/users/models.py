from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image
from django.dispatch import receiver
import os


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile image of user
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    # date of birth of user
    dob = models.DateField(blank=False, null=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize the image to size 300 x 300 before saving
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(models.signals.post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `UserProfile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(
                instance.image.path) and 'default.jpeg' not in old_image.path:
            os.remove(instance.image.path)


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