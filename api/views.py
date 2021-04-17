from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet

from activity.models import Activity
from user.models import Client

from api.serializers import ActivitySerializer, ChangePasswordSerializer
from api.serializers import RegistrationSerializer


class ActivityViewSet(ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = RegistrationSerializer


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            try:
                client = User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response({"email": ["El usuario no existe"]})

            if not client.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Contraseña antigua incorrecta"]}, status=status.HTTP_400_BAD_REQUEST)
            client.set_password(serializer.data.get("new_password"))
            client.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Contraseña guardada correctamente, nueva contraseña: ' + client.password,
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
