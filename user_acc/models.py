from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.username
