from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.utils.timezone import now


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_image', blank=True)
    age = models.PositiveIntegerField(default=18)

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_created+timedelta(hours=48):
            return False
        return True
