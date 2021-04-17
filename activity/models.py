from datetime import datetime

from django.db import models

from user.models import Organization, Organizer

from .validators import validate_file_extension


class ActivityType(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.name


class Activity(models.Model):
    STATUS_PENDING = 'P'
    STATUS_CHOICES = [(STATUS_PENDING, 'Pendiente'), ('C', 'Cancelada'), ('D', 'Finalizada')]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    photo = models.FileField(validators=[validate_file_extension], upload_to="activity", null=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.DO_NOTHING)
    start_date = models.DateField(default=datetime.now)
    start_time = models.TimeField(default=datetime.now)
    duration = models.FloatField()
    normal_price = models.FloatField()
    member_price = models.FloatField(null=True)
    number_participants = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default=STATUS_PENDING)
    location = models.CharField(max_length=100)
    only_member = models.BooleanField(default=False)
    organized_by = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=False, default=1)
    created_by = models.ForeignKey(Organizer, on_delete=models.DO_NOTHING, null=False, default=1)

    class Meta:
        verbose_name_plural = 'Activities'
        unique_together = ('activity_type', 'start_date', 'start_time', 'location', 'organized_by')


class InstructedBy(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.DO_NOTHING, null=False, default=1)
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING, null=False, default=1)

    class Meta:
        unique_together = ('activity', 'organizer')
