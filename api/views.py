from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet

from activity.models import Activity
from user.models import Client

from api.serializers import ActivitySerializer
from api.serializers import RegistrationSerializer


class ActivityViewSet(ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = RegistrationSerializer
