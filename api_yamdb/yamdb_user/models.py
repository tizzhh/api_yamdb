from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q


class YamdbUser(AbstractUser):
    class Roles(models.TextChoices):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'

    confirmation_code = models.CharField(max_length=5, null=True, blank=True)
    email = models.EmailField(
        unique=True, max_length=254, null=False, blank=False
    )
    bio = models.TextField('Биография', null=True, blank=True)
    role = models.CharField(
        'Роль', choices=Roles.choices, max_length=9, default=Roles.user
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(username='me'), name='username_me_banned_word'
            )
        ]
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username
