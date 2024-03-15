from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.constants import OBJECT_PER_ADMIN_PAGE
from reviews.models import YamdbUser

admin.site.empty_value_display = 'нет данных'
admin.site.site_title = 'Админ-зона проекта YAMDB'
admin.site.site_header = 'Админ-зона проекта YAMDB'


@admin.register(YamdbUser)
class UserAdmin(UserAdmin):
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
