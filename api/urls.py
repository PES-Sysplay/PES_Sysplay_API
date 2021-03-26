from django.urls import path, include
from rest_framework import routers

from api.views import ActivityViewSet

router = routers.DefaultRouter()
router.register(r'activity', ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
