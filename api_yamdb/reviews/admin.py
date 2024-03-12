from django.contrib import admin

from .constants import OBJECT_PER_ADMIN_PAGE
from .models import Category, Comment, Genre, Review, Title, YamdbUser

admin.site.empty_value_display = 'нет данных'
admin.site.site_title = 'Админ-зона проекта YAMDB'
admin.site.site_header = 'Админ-зона проекта YAMDB'


@admin.register(YamdbUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    list_display_links = ('username',)
    list_filter = ('username',)
    list_per_page = OBJECT_PER_ADMIN_PAGE
    search_fields = ('username', 'role')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    list_filter = ('name',)
    list_per_page = OBJECT_PER_ADMIN_PAGE
    search_field = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'review')
    list_display_links = ('text',)
    list_filter = ('pub_date', 'author')
    list_per_page = OBJECT_PER_ADMIN_PAGE
    search_field = ('author', 'review')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    list_filter = ('name',)
    list_per_page = OBJECT_PER_ADMIN_PAGE
    search_field = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'pub_date', 'author', 'score')
    list_display_links = ('title',)
    list_filter = ('pub_date', 'author', 'score', 'title')
    list_per_page = OBJECT_PER_ADMIN_PAGE
    search_field = ('author', 'title')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category')
    list_display_links = ('name',)
    list_filter = ('name', 'year', 'category')
    list_per_page = OBJECT_PER_ADMIN_PAGE
    search_field = ('name',)
