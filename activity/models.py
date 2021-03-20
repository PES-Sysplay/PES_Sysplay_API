from datetime import datetime

from django.db import models
from .validators import validate_file_extension


class ActivityType(models.Model):
    name = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return self.name


class Activity(models.Model):
    STATUS_DEFAULT = 'P'
    STATUS_CHOICES = [(STATUS_DEFAULT, 'Pendiente'), ('C', 'Cancelada'), ('D', 'Finalizada')]

    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    photo = models.FileField(validators=[validate_file_extension], upload_to="activity", null=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.DO_NOTHING)
    start_date = models.DateField(default=datetime.now)
    start_time = models.TimeField(default=datetime.now)
    duration = models.FloatField()
    normal_price = models.FloatField()
    member_price = models.FloatField(null=True)
    number_participants = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default=STATUS_DEFAULT)
    location = models.CharField(max_length=20)
    only_member = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Activities'
        unique_together = ('activity_type', 'start_date', 'start_time', 'location')
