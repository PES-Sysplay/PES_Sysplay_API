from django.urls import path, include
from rest_framework import routers

from api.views import ActivityViewSet, ClientViewSet, ChangePasswordView, ActivityTypeViewSet, UserClientView, \
    FavoriteActivityView, JoinActivityView, ReportActivityView, GoogleLoginView
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'activity', ActivityViewSet)
router.register(r'client', ClientViewSet)
router.register(r'activitytype', ActivityTypeViewSet)
router.register(r'favorite', FavoriteActivityView)
router.register(r'join', JoinActivityView)
router.register(r'report', ReportActivityView)

urlpatterns = [
    path('', include(router.urls)),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('me/', UserClientView.as_view(), name='client'),
    path('login/', views.obtain_auth_token),
    path('login/google/', GoogleLoginView.as_view()),
]
