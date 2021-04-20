from django.urls import path

from user.views import login, logout, OrganizerListView, InviteOrganizerView, DeleteUserView

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('manage/', OrganizerListView.as_view(), name='manage'),
    path('invite/', InviteOrganizerView.as_view(), name='invite_user'),
    path('delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),
]
