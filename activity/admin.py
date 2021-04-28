from django.contrib import admin

from activity.models import Activity, ActivityType, Joined


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Joined)
class Joined(admin.ModelAdmin):
    pass
