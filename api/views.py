from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.generics import UpdateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from activity.models import Activity, ActivityType, FavoriteActivity
from api.emails import send_email_verification
from user.mixins import ClientPermission
from user.models import Client

from api.serializers import ActivitySerializer, ChangePasswordSerializer, ActivityTypeSerializer, UserSerializer, \
    FavoriteActivitySerializer
from api.serializers import RegistrationSerializer


class ActivityViewSet(ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ClientPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('favorite', False):
            queryset = queryset.filter(favoriteactivity__client_id=self.request.user.id)
        return queryset


class ClientViewSet(CreateModelMixin, GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        client = serializer.save()
        url = self.request.build_absolute_uri(reverse('email_verification',
                                                      args=[client.user.id, client.token_verification]))
        send_email_verification(url, client)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    model = User
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ClientPermission]

    def get_object(self):
        try:
            return Client.objects.get(user=self.request.user).user
        except Client.DoesNotExist:
            raise PermissionDenied()


class ActivityTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = ActivityTypeSerializer
    queryset = ActivityType.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ClientPermission]


class UserClientView(RetrieveDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = UserSerializer
    model = User
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ClientPermission]

    def get_object(self):
        try:
            return Client.objects.get(user=self.request.user).user
        except Client.DoesNotExist:
            raise PermissionDenied()


class FavoriteActivityView(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    queryset = FavoriteActivity.objects.all()
    serializer_class = FavoriteActivitySerializer
    models = FavoriteActivity
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ClientPermission]

    def get_object(self):
        activity_id = self.kwargs.get('pk', '')
        return get_object_or_404(FavoriteActivity, activity_id=activity_id, client_id=self.request.user.id)



