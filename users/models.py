from PIL import Image
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default_profile_pic.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if (img.height > 200 or img.width > 200):
            tar_size = (300, 300)
            img.thumbnail(tar_size)
            img.save(self.image.path)

