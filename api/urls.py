from django.urls import path, include
from rest_framework import routers

from api.views import ActivityViewSet, ClientViewSet

router = routers.DefaultRouter()
router.register(r'activity', ActivityViewSet)
router.register(r'client', ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
