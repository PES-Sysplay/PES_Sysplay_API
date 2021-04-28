import uuid

from django.db import models

from django.contrib.auth.models import User

from activity.validators import validate_file_extension


class Organization(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    super_host = models.BooleanField(default=False)
    photo = models.FileField(validators=[validate_file_extension], upload_to="user", null=True)


class Organizer(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    admin = models.BooleanField()
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=False)


class Client(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token_verification = models.UUIDField(unique=True, default=uuid.uuid4)


class Favorites(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=False, default=1)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=False, default=1)

    class Meta:
        unique_together = ('client', 'organization')
