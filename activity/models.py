from django.db import models
from .validators import validate_file_extension


class Activity(models.Model):
    STATUS_CHOICES = [('P', 'Pendiente'), ('C', 'Cancelada'), ('D', 'Finalizada')]
    #   de momento porque no deja hacer migration (pide que se de un valor default)
    name = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=100)
    photo = models.FileField(validators=[validate_file_extension], upload_to="activity", null=True)
    start_time = models.DateTimeField()
    duration = models.FloatField()
    normal_price = models.FloatField()
    member_price = models.FloatField(null=True)
    number_participants = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    location = models.CharField(max_length=20)
    only_member = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Activities'
