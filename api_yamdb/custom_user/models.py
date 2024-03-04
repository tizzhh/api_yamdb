from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'

    email = models.CharField(unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', choices=Roles.choices, max_length=9, default=Roles.user
    )

    def __str__(self) -> str:
        return self.username
