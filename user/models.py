import uuid

from django.db import models

from django.contrib.auth.models import User

from activity.validators import validate_file_extension


class Organization(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    super_host = models.BooleanField(default=False)
    photo = models.FileField(validators=[validate_file_extension], upload_to="user", null=True)

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

    def __str__(self):
        return self.user.username
