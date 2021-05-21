from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.generics import UpdateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from activity.models import Activity, ActivityType, FavoriteActivity
from activity_action.models import ActivityJoined, ActivityReport, ActivityReview
from api.emails import send_email_verification, send_remainder_email
from user.mixins import ClientPermission
from user.models import Client, Blocked

from api.serializers import ActivitySerializer, ChangePasswordSerializer, ActivityTypeSerializer, UserSerializer, \
    FavoriteActivitySerializer, ActivityJoinedSerializer, ReportActivitySerializer, ReviewActivitySerializer, \
    ProfileSerializer
from api.serializers import RegistrationSerializer
from user.services import GoogleOauth


class ActivityViewSet(ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [ClientPermission]

    def get_queryset(self):
        queryset = super().get_queryset().exclude(status=Activity.STATUS_CANCELLED)
        if self.request.GET.get('favorite', False):
            queryset = queryset.filter(favoriteactivity__client_id=self.request.user.id)
        if self.request.GET.get('joined', False):
            queryset = queryset.filter(activityjoined__client_id=self.request.user.id)
        blocked = Blocked.objects.filter(client_id=self.request.user.id).values_list('organization_id', flat=True)
        queryset = queryset.exclude(organized_by__in=blocked)
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
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [ClientPermission]

    def get_object(self):
        try:
            return Client.objects.get(user=self.request.user).user
        except Client.DoesNotExist:
            raise PermissionDenied()


class ActivityTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = ActivityTypeSerializer
    queryset = ActivityType.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [ClientPermission]


class UserClientView(UpdateModelMixin, RetrieveDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = UserSerializer
    model = User
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [ClientPermission]

    def get_object(self):
        try:
            return Client.objects.get(user=self.request.user).user
        except Client.DoesNotExist:
            raise PermissionDenied()

    def put(self, request):
        return self.update(request)


class ActionActivityView(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    queryset = None
    serializer_class = None
    models = None
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [ClientPermission]

    def get_object(self):
        activity_id = self.kwargs.get('pk', '')
        return get_object_or_404(self.models, activity_id=activity_id, client_id=self.request.user.id,
                                 activity__status=Activity.STATUS_PENDING)


class FavoriteActivityView(ActionActivityView):
    queryset = FavoriteActivity.objects.all()
    serializer_class = FavoriteActivitySerializer
    models = FavoriteActivity


class JoinActivityView(ActionActivityView):
    queryset = ActivityJoined.objects.all()
    serializer_class = ActivityJoinedSerializer
    models = ActivityJoined

    def perform_create(self, serializer):
        super().perform_create(serializer)
        activity_id = serializer.validated_data.get('activity_id', '')
        activity = Activity.objects.filter(id=activity_id).annotate(count=Count('activityjoined'))[0]
        if activity.count == activity.number_participants - 2:
            send_remainder_email(activity)


class ActionInsideActivityView(ActionActivityView):
    def get_object(self):
        activity_id = self.kwargs.get('pk', '')
        return get_object_or_404(self.models, joined__activity_id=activity_id, joined__client_id=self.request.user.id)


class ReportActivityView(ActionInsideActivityView):
    queryset = ActivityReport.objects.all()
    serializer_class = ReportActivitySerializer
    models = ActivityReport


class ReviewActivityView(ListModelMixin, ActionInsideActivityView):
    queryset = ActivityReview.objects.all()
    serializer_class = ReviewActivitySerializer
    models = ActivityReview

    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.request.GET.get('organization', None)
        if not organization:
            raise Http404
        queryset = queryset.filter(joined__activity__organized_by=organization)
        return queryset


class GoogleLoginView(APIView):
    def get(self, request):
        token = request.GET.get('token', '')
        if not token:
            return HttpResponseBadRequest('Invalid token')
        try:
            email = GoogleOauth(token=token).get_email()
        except GoogleOauth.InvalidToken:
            return HttpResponseBadRequest('Invalid token')
        try:
            client = Client.objects.get(user__username=email)
        except Client.DoesNotExist:
            client = Client.create_client_from_google(email=email)
        token = client.get_token()
        return JsonResponse({'token': token})


class ProfileView(UpdateAPIView, APIView):
    queryset = Client.objects.all()
    serializer_class = ProfileSerializer
    model = Client
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [ClientPermission]

    def get_object(self):
        return self.request.user.client
