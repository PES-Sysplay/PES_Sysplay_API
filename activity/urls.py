from django.urls import path

from activity.views import CreateActivityView

urlpatterns = [
    path('view/', CreateActivityView.as_view(), name='create_activity')
]
