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
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'student_id', 'date_of_birth', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_staff', 'is_active')}
        )
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(MyUser, CustomUserAdmin)

