import uuid

from django.db import models

from django.contrib.auth.models import User
from django.db.models import Avg, Count
from rest_framework.authtoken.models import Token

from activity.validators import validate_file_extension


class Organization(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    photo = models.FileField(validators=[validate_file_extension], upload_to="user", null=True)

    @property
    def rank(self):
        average = self.activity_set.values('organized_by').aggregate(
            average=Avg('activityjoined__activityreview__stars')).get('average', 0)
        count_neg = self.activity_set.values('organized_by').aggregate(
            count=Count('activityjoined__activityreport')).get('count', 0)
        count_pos = self.activity_set.values('organized_by').filter(activityjoined__activityreview__stars__gte=4) \
            .aggregate(count=Count('activityjoined__activityreview')).get('count', 1)
        if average is None:
            average = 0
        if count_pos is None:
            count_pos = 1
        if count_neg is None:
            count_neg = 0
        count_pos += int(count_pos == 0)
        return average - (count_neg / count_pos)

    @property
    def superhost(self):
        return self.rank >= 3.5

    def __str__(self):
        return self.name


class Organizer(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    admin = models.BooleanField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.user.username


class Client(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token_verification = models.UUIDField(unique=True, default=uuid.uuid4)
    email = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_token(self):
        try:
            return Token.objects.get(user_id=self.user_id).key
        except Token.DoesNotExist:
            token = Token(user_id=self.user_id)
            token.save()
            return token

    @staticmethod
    def create_client_from_google(email):
        user = User(username=email, password='', email=email)
        user.save()
        client = Client(user=user, is_verified=True)
        client.save()
        return client


class Blocked(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.organization, self.client)

    class Meta:
        unique_together = ('organization', 'client')
