from django.urls import path

from activity_action.views import CheckinView, BlockUserView, UnblockUserView, ReviewsView, RemoveReview

urlpatterns = [
    path('<int:id>/list/', CheckinView.as_view(), name='checkin-list'),
    path('<int:id>/<int:uid>/block/', BlockUserView.as_view(), name='block-user'),
    path('<int:id>/<int:uid>/unblock/', UnblockUserView.as_view(), name='unblock-user'),
    path('<int:id>/reviews/', ReviewsView.as_view(), name='reviews'),
    path('<int:id>/remove/', RemoveReview.as_view(), name='remove-review'),

]
