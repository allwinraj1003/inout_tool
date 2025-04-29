from django.contrib import admin
from .models import Attendance, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import site


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')  # Add first_name and last_name here
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'role')}),  # Add first_name and last_name here
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )


    # VERY IMPORTANT: remove username field from UserAdmin behavior
    add_form_template = None

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date','user', 'role', 'check_in_time', 'check_out_time')
    list_filter = ('role', 'date')
    search_fields = ('user_email', 'role')
    ordering = ('-date',)
    


