from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False


class UserAdmin(DefaultUserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines = ()

        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = (UserProfileInline,)

        return super(UserAdmin, self).change_view(*args, **kwargs)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
