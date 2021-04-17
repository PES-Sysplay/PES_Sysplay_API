from django.urls import path, include
from rest_framework import routers

from api.views import ActivityViewSet
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'activity', ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', views.obtain_auth_token),
]
