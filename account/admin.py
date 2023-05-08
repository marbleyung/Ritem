from django.contrib import admin
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone']
    fields = ('username', 'email', 'phone', 'password', 'first_name', 'last_name')


admin.site.register(CustomUser, CustomUserAdmin)
