from django.contrib import admin
from . models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_editable = ['is_staff','is_active','username']
    list_display = ['username','is_superuser', 'email', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'lastname', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions',)}),
    )






admin.site.register(User)
admin.site.register(Support)

