from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.DO_NOTHING)
