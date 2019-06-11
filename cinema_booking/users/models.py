from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile image of user
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    # date of birth of user
    dob = models.DateField(blank=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Resize the image to size 300 x 300 before saving
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)