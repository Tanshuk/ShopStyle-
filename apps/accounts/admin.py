from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Customised User admin panel."""

    # Columns shown in the list view
    list_display = (
        'avatar_thumbnail', 'email', 'get_full_name',
        'phone', 'is_email_verified', 'is_staff', 'date_joined'
    )
    list_display_links = ('email', 'get_full_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_email_verified')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at', 'avatar_thumbnail')

    # Field layout on the detail/edit page
    fieldsets = (
        ('Login Info',   {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': (
            'avatar_thumbnail', 'avatar',
            'first_name', 'last_name', 'phone', 'date_of_birth'
        )}),
        ('Verification', {'fields': ('is_email_verified',)}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps',   {'fields': ('date_joined', 'last_login', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    # Fields shown when creating a NEW user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">',
                obj.avatar.url
            )
        return format_html(
            '<div style="width:40px;height:40px;border-radius:50%;background:#FF3F6C;'
            'display:flex;align-items:center;justify-content:center;color:white;'
            'font-weight:bold;font-size:14px;">{}</div>',
            obj.get_short_name()[0].upper() if obj.get_short_name() else '?'
        )
    avatar_thumbnail.short_description = 'Avatar'