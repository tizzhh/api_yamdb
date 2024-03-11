from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q


class YamdbUser(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    password = None
    confirmation_code = models.CharField(max_length=5, null=True, blank=True)
    email = models.EmailField(
        unique=True, max_length=254, null=False, blank=False
    )
    bio = models.TextField('Биография', null=True, blank=True)
    role = models.CharField(
        'Роль',
        choices=Roles.choices,
        max_length=max(len(role[0]) for role in Roles.choices),
        default=Roles.USER,
    )

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(username='me'), name='username_me_banned_word'
            )
        ]
        ordering = ('email',)

    def __str__(self) -> str:
        return self.username
