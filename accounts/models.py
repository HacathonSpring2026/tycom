from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    first_name = None
    last_name = None

    username = models.CharField(max_length=150, unique=False)

    email = models.EmailField(unique=True)

    class Meta:
        verbose_name_plural = "CustomUser"


# Create your models here.
