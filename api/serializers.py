import datetime

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from activity.models import Activity, ActivityType, FavoriteActivity
from activity_action.models import ActivityJoined, ActivityReport, ActivityReview
from chat.models import Message, Chat

from user.models import Client, Organization


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    photo_url = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    date_time = serializers.SerializerMethodField()
    date_time_finish = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()
    clients_joined = serializers.SerializerMethodField()
    checked_in = serializers.SerializerMethodField()
    reported = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()
    superhost = serializers.SerializerMethodField()

    def get_token(self, activity):
        request = self.context.get('request')
        joined = activity.activityjoined_set.filter(client_id=request.user.id)
        if len(joined) == 0:
            return None
        return joined[0].token

    def get_date_time(self, activity):
        date_time = datetime.datetime.combine(activity.start_date, activity.start_time)
        return date_time.strftime("%b %d, %Y, %H:%M")

    def get_date_time_finish(self, activity):
        date_time = datetime.datetime.combine(activity.start_date, activity.start_time)
        date_time = date_time + datetime.timedelta(minutes=activity.duration)
        return date_time.strftime("%b %d, %Y, %H:%M")

    def get_status(self, activity):
        return activity.get_status_display()

    def get_photo_url(self, activity):
        request = self.context.get('request')
        photo_url = activity.photo.url
        return request.build_absolute_uri(photo_url)

    def get_organization(self, activity):
        return activity.organized_by.name

    def get_created(self, activity):
        return activity.created_by.user.first_name

    def get_timestamp(self, activity):
        date_time = datetime.datetime.combine(activity.start_date, activity.start_time)
        return date_time.timestamp()

    def get_favorite(self, activity):
        request = self.context.get('request')
        return activity.favoriteactivity_set.filter(client_id=request.user.id).exists()

    def get_joined(self, activity):
        request = self.context.get('request')
        return activity.activityjoined_set.filter(client_id=request.user.id).exists()

    def get_clients_joined(self, activity):
        return activity.activityjoined_set.count()

    def get_checked_in(self, activity):
        request = self.context.get('request')
        joined = activity.activityjoined_set.filter(client_id=request.user.id)
        if len(joined) > 0:
            return joined[0].checked_in
        return False

    def get_reported(self, activity):
        request = self.context.get('request')
        joined = activity.activityjoined_set.filter(client_id=request.user.id)
        if len(joined) > 0:
            return ActivityReport.objects.filter(joined=joined[0].id).exists()
        return False

    def get_superhost(self, activity):
        return activity.organized_by.superhost

    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'photo_url', 'activity_type_id', 'date_time', 'duration',
                  'normal_price', 'member_price', 'number_participants', 'status', 'location', 'only_member',
                  'organization', 'created', 'timestamp', 'favorite', 'joined', 'clients_joined', 'checked_in',
                  'reported', 'token', 'date_time_finish', 'superhost']


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, client):
        token = Token.objects.get(user__username=client.get('user').get('username')).key
        return token

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
        Token(user=user).save()
        return client

    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'token']


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get("old_password")):
            instance.set_password(validated_data.get("new_password"))
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("Password error")

    class Meta:
        model = User
        fields = ['old_password', 'new_password']


class ActivityTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = ActivityType
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    favorites = serializers.SerializerMethodField(read_only=True)
    joined = serializers.SerializerMethodField(read_only=True)
    email_notifications = serializers.BooleanField(write_only=True)
    notifications = serializers.BooleanField(source='client.email', read_only=True)

    def get_favorites(self, user):
        return user.client.favoriteactivity_set.count()

    def get_joined(self, user):
        return user.client.activityjoined_set.count()

    def update(self, instance, validated_data):
        noty = validated_data.get('email_notifications', None)
        user = super().update(instance, validated_data)
        user.client.email = noty
        user.client.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'username', 'favorites', 'joined', 'email_notifications', 'notifications']


class ActionActivitySerializer(serializers.ModelSerializer):
    activity_id = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['client_id'] = request.user.id
        return super().create(validated_data)

    class Meta:
        fields = ['activity_id']


class FavoriteActivitySerializer(ActionActivitySerializer):
    class Meta(ActionActivitySerializer.Meta):
        model = FavoriteActivity


class ActivityJoinedSerializer(ActionActivitySerializer):
    class Meta(ActionActivitySerializer.Meta):
        model = ActivityJoined

    def create(self, validated_data):
        activity_id = validated_data.get('activity_id', '')
        activity = get_object_or_404(Activity, id=activity_id)
        if activity.number_participants < activity.activityjoined_set.count() + 1:
            raise serializers.ValidationError({"detail": "Activity full"})
        return super().create(validated_data)


class ActionActivitySerializer(serializers.ModelSerializer):
    activity_id = serializers.IntegerField(source='joined__activity_id', required=False)
    joined_id = serializers.IntegerField(required=False, write_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        activity_id = validated_data.get('joined__activity_id', '')
        joined = get_object_or_404(ActivityJoined, activity_id=activity_id, client_id=request.user.id, checked_in=True)
        try:
            self.Meta.model.objects.get(joined_id=joined.id)
            raise Http404
        except self.Meta.model.DoesNotExist:
            pass
        del validated_data['joined__activity_id']
        validated_data['joined_id'] = joined.id
        return super().create(validated_data)


class ReportActivitySerializer(ActionActivitySerializer):
    class Meta:
        fields = ['activity_id', 'comment', 'joined_id']
        model = ActivityReport


class ReviewActivitySerializer(ActionActivitySerializer):
    class Meta:
        fields = ['activity_id', 'comment', 'joined_id', 'stars']
        model = ActivityReview


class MessageSerializer(serializers.ModelSerializer):
    date_timestamp = serializers.SerializerMethodField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    activity_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user_id'] = request.user.id
        activity_id = validated_data.get('activity_id', '')
        if activity_id:
            del validated_data['activity_id']
        try:
            chat = Chat.objects.get(client_id=request.user.id, activity_id=activity_id)
        except Chat.DoesNotExist:
            try:
                chat = Chat(client_id=request.user.id, activity_id=activity_id)
                chat.save()
            except IntegrityError:
                raise serializers.ValidationError('This activity does not exists')
        validated_data['chat_id'] = chat.id
        return super().create(validated_data)

    def get_date_timestamp(self, message):
        return message.date.timestamp()

    class Meta:
        fields = ['id', 'text', 'username', 'date_timestamp', 'activity_id']
        model = Message


class ChatSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='client.user.username', read_only=True)
    activity_name = serializers.CharField(source='activity.name', read_only=True)
    organization = serializers.CharField(source='activity.organized_by_id', read_only=True)
    organization_photo = serializers.SerializerMethodField(read_only=True)
    new = serializers.SerializerMethodField(read_only=True)

    def get_organization_photo(self, chat):
        request = self.context.get('request')
        photo_url = chat.activity.organized_by.photo.url
        return request.build_absolute_uri(photo_url)

    def get_new(self, chat):
        return not hasattr(chat.last_message.user, 'client')

    class Meta:
        fields = ['username', 'activity_id', 'activity_name', 'organization', 'id', 'new', 'organization_photo']
        model = Chat


class ChatSerializerExtended(ChatSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta(ChatSerializer.Meta):
        fields = ['username', 'activity_id', 'activity_name', 'organization', 'id', 'new', 'organization_photo',
                  'messages']


class OrganizationSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField(read_only=True)
    rank = serializers.SerializerMethodField(read_only=True)
    superhost = serializers.SerializerMethodField(read_only=True)

    def get_photo(self, organization):
        request = self.context.get('request')
        photo_url = organization.photo.url
        return request.build_absolute_uri(photo_url)

    def get_rank(self, organization):
        return organization.rank

    def get_superhost(self, organization):
        return organization.superhost

    class Meta:
        model = Organization
        fields = ['name', 'photo', 'rank', 'superhost']
