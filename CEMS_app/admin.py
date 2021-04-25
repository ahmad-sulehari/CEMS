from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


admin.site.register(Game)
admin.site.register(Event)

admin.site.index_title = 'Sports Society EMS'
admin.site.site_header = 'Admin Portal'
admin.site.site_title = 'EMS Administration'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = ('student_id', 'email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'student_id', 'date_of_birth', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser', 'groups', 'user_permissions')}), # adding groups and user_permissions solves the problem of groups and permissions not showing for custom user models.
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_staff', 'is_active')}
        )
    )
    search_fields = ('student_id',)
    ordering = ('student_id',)


admin.site.register(MyUser, CustomUserAdmin)

