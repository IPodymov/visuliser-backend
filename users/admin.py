from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профиль"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_role",
    )
    list_select_related = ("profile",)

    def get_role(self, instance):
        return instance.profile.get_role_display()

    get_role.short_description = "Роль"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
