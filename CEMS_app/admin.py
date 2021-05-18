from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy
from .models import *
from grappelli.settings import *

MyUser = get_user_model()

ADMIN_TITLE = 'CEMS Admin'
ADMIN_HEADLINE = 'CEMS Admin'


admin.site.site_title = 'EMS Administration'
admin.site.index_title = 'Sports Society EMS'
admin.site.site_header = 'Admin Portal'


@admin.register(MyUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = ('student_id', 'email', 'is_staff', 'is_active', 'is_superuser', 'phone_number') # list of item to be displayed | use id for default primary key
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('degree', 'section', 'session', 'student_id_number', 'student_id', 'date_of_birth', 'gender', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser', 'groups')}), # , 'user_permissions' adding groups and user_permissions solves the problem of groups and permissions not showing for custom user models.
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_staff', 'is_active')}
        )
    )
    search_fields = ('student_id',)
    ordering = ('student_id',)

#
# admin.site.unregister(MyUser)
# admin.site.register(MyUser, UserAdmin)
# admin.site.register(StaffProxyModel, CustomUserAdmin)


def has_superuser_permission(request):
    return request.user.is_active and request.user.is_superuser


admin.site.has_permission = has_superuser_permission


# staff admin site
class StaffAdminSite(AdminSite):
    pass


staff_admin_site = StaffAdminSite(name='staff_admin')
staff_admin_site.site_header = 'Staff Admin'


@admin.register(Item, Game, Event, site=staff_admin_site)
class StaffAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment, site=staff_admin_site)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'game_id', 'payment_type', 'amount', 'submission_date', 'status', 'verification_date')
    list_filter = ('game_id', 'status', 'event_id', 'user_id')


'''
class GameAdminSite(AdminSite):
    site_header = 'Game Admin'


game_admin_site = GameAdminSite(name='game_admin')


@admin.register(Game, site=game_admin_site)
class GameAdmin(admin.ModelAdmin):
    pass
'''