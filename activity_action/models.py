from datetime import datetime

from django.db import models

from activity.models import Activity
from user.models import Client


class ActivityJoined(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ('activity', 'client')
