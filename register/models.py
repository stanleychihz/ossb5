from django.conf import settings
from django.db import models

class Static(models.Model):

    img = models.ImageField(blank=True, upload_to='register_images/')

def __str__(self):

    return self.img

