from django.urls import path

from activity_action.views import CheckinView

urlpatterns = [
    path('<int:id>/list/', CheckinView.as_view(), name='checkin-list'),
]
