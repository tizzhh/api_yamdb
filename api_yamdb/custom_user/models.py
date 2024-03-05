from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'

    email = models.EmailField(unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', choices=Roles.choices, max_length=9, default=Roles.user
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(username='me'), name='username_me_banned_word'
            )
        ]

    def __str__(self) -> str:
        return self.username
