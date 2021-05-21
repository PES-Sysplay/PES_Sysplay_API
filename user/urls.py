from django.urls import path

from user.views import login, logout, OrganizerListView, InviteOrganizerView, DeleteUserView, verification_email, \
    ProfileView, ChangePassword

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('manage/', OrganizerListView.as_view(), name='manage'),
    path('invite/', InviteOrganizerView.as_view(), name='invite_user'),
    path('delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('me/change_password/', ChangePassword.as_view(), name='change_password'),
    path('verify_mail/<int:id>/<uuid:token>/',
         verification_email, name='email_verification'),
]
