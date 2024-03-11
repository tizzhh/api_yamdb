# Generated by Django 3.2 on 2024-03-11 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_title_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'default_related_name': 'titles', 'ordering': ('name', 'year', 'category')},
        ),
        migrations.RemoveConstraint(
            model_name='title',
            name='Год выпуска не может быть больше текущего',
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(verbose_name='Год публикации'),
        ),
    ]
