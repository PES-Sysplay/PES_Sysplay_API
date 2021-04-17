from django.urls import path

from activity.views import ActivityCreate, ActivityView, ActivityEdit, ActivityListView

urlpatterns = [
    path('create/', ActivityCreate.as_view(), name='create_activity'),
    path('<int:id>/view/', ActivityView.as_view(), name='view_activity'),
    path('<int:id>/edit/', ActivityEdit.as_view(), name='edit_activity'),
    path('all/', ActivityListView.as_view(), name='activity_list_view'),
]
