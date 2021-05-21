from django.contrib import admin
from .models import Organization, Organizer, Client, Blocked


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Blocked)
class BlockedAdmin(admin.ModelAdmin):
    pass
