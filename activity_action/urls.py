from django.urls import path

from activity_action.views import CheckinView, BlockUserView, UnblockUserView

urlpatterns = [
    path('<int:id>/list/', CheckinView.as_view(), name='checkin-list'),
    path('<int:id>/<int:uid>/block/', BlockUserView.as_view(), name='block-user'),
    path('<int:id>/<int:uid>/unblock/', UnblockUserView.as_view(), name='unblock-user'),
]
