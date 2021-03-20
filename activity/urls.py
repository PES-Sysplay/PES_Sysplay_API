from django.urls import path

from activity.views import ActivityCreate, ActivityView, ActivityEdit

urlpatterns = [
    path('create/', ActivityCreate.as_view(), name='create_activity'),
    path('<int:id>/view/', ActivityView.as_view(), name='view_activity'),
    path('<int:id>/edit/', ActivityEdit.as_view(), name='edit_activity'),

]
