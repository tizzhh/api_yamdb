import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q

USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254


# переместил сюда из-за циклического импорта
class BaseUserValidator:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Username cannot be "me"')
        if banned_symbols := re.sub(r'[\w.@+-]+', '', value):
            raise ValidationError(
                f'Prohibited username symbols: \'{banned_symbols}\''
            )
        return value


class YamdbUser(AbstractUser, BaseUserValidator):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(
        unique=True, max_length=EMAIL_MAX_LENGTH, null=False, blank=False
    )
    bio = models.TextField('Биография', blank=True)
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
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
