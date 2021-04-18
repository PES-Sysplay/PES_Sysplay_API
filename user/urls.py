from django.urls import path

from user.views import login, logout, OrganizerListView

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('manage/', OrganizerListView.as_view(), name='manage')
]
