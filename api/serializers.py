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
                  'normal_price', 'member_price', 'number_participants', 'status', 'location', 'only_member', 'organized_by', 'created_by']


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Client
        fields = ['username', 'email', 'password']

    def save(self):
        user = User(
            email=self.validated_data['user']['email'],
            username=self.validated_data['user']['username'],
        )

        password = self.validated_data['user']['password']
        user.set_password(password)
        client = Client(
            user=user
        )
        user.save()
        client.save()
        return client


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    email = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
