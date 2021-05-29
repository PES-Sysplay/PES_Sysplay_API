import uuid
from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from activity.models import Activity
from user.models import Client


class ActivityJoined(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    checked_in = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return '%s - %s' % (self.client.user.username, self.activity)

    class Meta:
        unique_together = ('activity', 'client')
        verbose_name_plural = 'Activity Joined'


class ActivityReport(models.Model):
    joined = models.OneToOneField(ActivityJoined, on_delete=models.CASCADE, primary_key=True)
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.joined)


class ActivityReview(models.Model):
    joined = models.OneToOneField(ActivityJoined, on_delete=models.CASCADE, primary_key=True)
    comment = models.CharField(max_length=1000, blank=True, verbose_name='commentarios')
    stars = models.FloatField(validators=[MaxValueValidator(5), MinValueValidator(0)], verbose_name='puntuación')

    def __str__(self):
        return str(self.joined)


class ReportActivityReview(models.Model):
    review = models.ForeignKey(ActivityReview, on_delete=models.CASCADE, related_name='reports')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.client) + ' - ' + str(self.review)

    class Meta:
        unique_together = ('review', 'client')
