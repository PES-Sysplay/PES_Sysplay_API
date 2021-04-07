from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

    @api_view(['POST', ])
    def registration_view(request):
        if request.method == 'POST':
            serializer = RegistrationSerializer(data=request.data)
            data = {}
        if serializer.is_valid():
            client = serializer.save()
            data['response'] = "Usuario registrado correctamente"
            data['email'] = client.email
            data['username'] = client.username
            data['password'] = client.password
        else:
            data = serializer.errors
        return Response(data)
