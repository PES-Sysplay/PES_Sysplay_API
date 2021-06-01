from django.urls import path, include
from rest_framework import routers

from api.views import ActivityViewSet, ClientViewSet, ChangePasswordView, ActivityTypeViewSet, UserClientView, \
    FavoriteActivityView, JoinActivityView, ReportActivityView, ReviewActivityView, GoogleLoginView, ChatView, \
    MessageView, OrganizationView, ReportActivityReviewView

from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'activity', ActivityViewSet)
router.register(r'client', ClientViewSet)
router.register(r'activitytype', ActivityTypeViewSet)
router.register(r'favorite', FavoriteActivityView)
router.register(r'join', JoinActivityView)
router.register(r'report', ReportActivityView)
router.register(r'review', ReviewActivityView)
router.register(r'chat', ChatView)
router.register(r'message', MessageView)
router.register(r'organization', OrganizationView)
router.register(r'report_review', ReportActivityReviewView)

urlpatterns = [
    path('', include(router.urls)),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('me/', UserClientView.as_view(), name='client'),
    path('login/', views.obtain_auth_token),
    path('login/google/', GoogleLoginView.as_view()),
]
