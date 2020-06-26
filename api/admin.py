from django.contrib import admin

from .models import HotlineUser, Level
# Register your models here.
admin.site.register(HotlineUser)
admin.site.register(Level)
