from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser

from .models import HotlineUser
# Register your models here.
admin.site.register(HotlineUser)