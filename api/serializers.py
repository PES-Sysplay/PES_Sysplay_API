from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from activity.models import Activity

from user.models import Client


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    photo_url = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    date_time = serializers.SerializerMethodField()

    def get_date_time(self, activity):
        date_time = datetime.combine(activity.start_date, activity.start_time)
        return date_time.strftime("%b %d, %Y, %H:%M")

    def get_status(self, activity):
        return activity.get_status_display()

    def get_photo_url(self, activity):
        request = self.context.get('request')
        photo_url = activity.photo.url
        return request.build_absolute_uri(photo_url)

    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'photo_url', 'activity_type_id', 'date_time', 'duration',
                  'normal_price', 'member_price', 'number_participants', 'status', 'location', 'only_member']


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'password2']

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden.'})
        user.password = password

        client = Client(
            user=user
        )
        user.save()
        client.save()
        return client
