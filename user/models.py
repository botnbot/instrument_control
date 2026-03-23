from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name}_{self.last_name}"
