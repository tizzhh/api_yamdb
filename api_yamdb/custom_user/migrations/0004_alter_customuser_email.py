# Generated by Django 3.2 on 2024-03-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('custom_user', '0003_auto_20240304_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
