from django.contrib import admin

from activity_action.models import ActivityJoined, ActivityReport


@admin.register(ActivityJoined)
class ActivityJoinedAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityReport)
class ActivityReportAdmin(admin.ModelAdmin):
    pass
