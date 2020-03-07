from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import Group
from .models import User

# Register your models here.


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'get_short_name')
    list_filter = ('is_staff',)

    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ("Personal Details", {'fields':('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('name', 'company_name', 'email', 'password1', 'password2')}),)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
# admin.site.register(Group)