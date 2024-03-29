# Generated by Django 3.2 on 2024-03-13 10:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1, 'Оценка не может быть ниже 1.'
                    ),
                    django.core.validators.MaxValueValidator(
                        10, 'Оценка не может быть выше 10.'
                    ),
                ],
                verbose_name='Оценка',
            ),
        ),
    ]
