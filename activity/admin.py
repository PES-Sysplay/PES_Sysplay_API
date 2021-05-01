from django.contrib import admin

from activity.models import Activity, ActivityType, FavoriteActivity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(FavoriteActivity)
class FavoriteActivityAdmin(admin.ModelAdmin):
    pass
