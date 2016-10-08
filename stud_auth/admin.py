from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User

from stud_auth.models import StProfile


class StProfileInline(admin.StackedInline):
    model = StProfile


class UserAdmin(auth_admin.UserAdmin):
    inlines = (StProfileInline,)

# replace existing User admin form
admin.site.unregister(User)
admin.site.register(User,  UserAdmin)
