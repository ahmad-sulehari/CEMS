from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.http import HttpResponse
from .models import *
import csv

MyUser = get_user_model()


admin.site.site_title = 'EMS Administration'
admin.site.index_title = 'Sports Society EMS'
admin.site.site_header = 'Admin Portal'


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(MyUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    # list of item to be displayed | use id for default primary key
    list_display = ('student_id', 'email', 'is_staff', 'is_active', 'is_superuser', 'phone_number', 'is_verified')
    list_filter = ('email', 'is_staff', 'is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': (
            'degree', 'section', 'session', 'student_id_number',
            'student_id', 'date_of_birth', 'gender', 'profile_image'
        )}
        ),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser', 'groups')
        }),  # can add for display: adding groups and user_permissions.
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('student_id',)
    ordering = ('student_id',)


admin.site.unregister(Group)
admin.site.register(Media)
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


@admin.register(Item, site=staff_admin_site)
class ItemAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'quantity', 'allocated', 'cost', 'damaged')
    search_fields = ('name',)
    actions = ['export_as_csv']


@admin.register(Payment, site=staff_admin_site)
class PaymentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'user_id', 'game_id', 'payment_type',
        'amount', 'submission_date', 'status',
        'tid', 'verification_date'
    )
    list_filter = (
        'event_id', 'game_id', 'status', 'payment_type'
    )
    search_fields = ('tid',)
    actions = ['export_as_csv']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event_id":
            kwargs["queryset"] = Event.objects.filter(is_active=True)
        if db_field.name == "game_id":
            kwargs["queryset"] = Game.objects.filter(is_active=True)
        if db_field.name == 'user_id':
            kwargs["queryset"] = MyUser.objects.filter(is_active=True).filter(is_verified=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Game, site=staff_admin_site)
class GameAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('title', 'event_id', 'team_size', 'registration_fee')
    list_filter = ('event_id', 'is_active')
    search_fields = ('title',)
    actions = ['export_as_csv']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event_id":
            kwargs["queryset"] = Event.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'payment_account_number')
    list_filter = ('is_active',)


@admin.register(GameCoordinator, site=staff_admin_site)
class HeadCoordinatorAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user_id', 'game_id')
    actions = ['export_as_csv']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "game_id":
            kwargs["queryset"] = Game.objects.filter(is_active=True)
        if db_field.name == 'user_id':
            kwargs["queryset"] = MyUser.objects.filter(is_active=True).filter(is_verified=True).filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Team, site=staff_admin_site)
class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'team_lead', 'team_name', 'team_size']
    search_fields = ['team_id']
    fieldsets = (
        (None, {'fields': ('team_lead', 'team_name')}),
    )


@admin.register(RequiredItems, site=staff_admin_site)
class RequiredItems(admin.ModelAdmin):
    list_display = ['item_id', 'quantity']


@admin.register(Volunteer, site=staff_admin_site)
class RequiredItems(admin.ModelAdmin):
    list_display = ['user_id', 'skill', 'available']


@admin.register(Expenditure, site=staff_admin_site)
class RequiredItems(admin.ModelAdmin):
    list_display = ['staff_id', 'amount_spent', 'purpose']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'staff_id':
            kwargs["queryset"] = MyUser.objects.filter(is_active=True).filter(is_verified=True).filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ItemIssued, site=staff_admin_site)
class RequiredItems(admin.ModelAdmin):
    list_display = ['item_id', 'game_id', 'quantity', 'damaged', 'game_coordinator_id', 'time_of_issue', 'return_time']
