from django.urls import path

from activity.views import ActivityCreate

urlpatterns = [
    path('view/', ActivityCreate.as_view(), name='create_activity'),
]
