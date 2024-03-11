from django.contrib import admin

from reviews.models import YamdbUser


class YamdbUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    search_fields = ('username', 'email', 'role')
    list_filter = 'role'
    empty_value_display = '-пусто-'


admin.site.register(YamdbUser)
