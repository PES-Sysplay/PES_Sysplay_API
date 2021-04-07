from django.contrib import admin

from user.models import Client


@admin.register(Client)
class ActivityAdmin(admin.ModelAdmin):
    pass
