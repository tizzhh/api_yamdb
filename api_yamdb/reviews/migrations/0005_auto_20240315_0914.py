# Generated by Django 3.2 on 2024-03-15 09:14

from django.db import migrations, models

import reviews.validators


class Migration(migrations.Migration):
    dependencies = [
        ('reviews', '0004_auto_20240313_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(
                validators=[reviews.validators.validate_year],
                verbose_name='Год публикации',
            ),
        ),
    ]
