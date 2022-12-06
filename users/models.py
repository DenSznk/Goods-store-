from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model extension"""

    image = models.ImageField(upload_to='user_images', null=True, blank=True)
