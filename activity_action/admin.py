from django.contrib import admin

from activity_action.models import ActivityJoined


@admin.register(ActivityJoined)
class ActivityJoinedAdmin(admin.ModelAdmin):
    pass
