# Generated by Django 3.2 on 2024-03-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_moderator',
        ),
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Биография'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(
                choices=[
                    ('user', 'User'),
                    ('moderator', 'Moderator'),
                    ('admin', 'Admin'),
                ],
                default='user',
                max_length=9,
                verbose_name='Роль',
            ),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.CharField(max_length=254, unique=True),
        ),
    ]