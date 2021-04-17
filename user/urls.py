from django.urls import path

from user.views import login, logout

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
