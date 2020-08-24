from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
# from account.models import Profile
# from account.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(get_user_model(), UserAdmin)