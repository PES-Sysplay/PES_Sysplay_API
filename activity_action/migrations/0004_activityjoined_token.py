# Generated by Django 3.1.7 on 2021-05-08 10:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('activity_action', '0003_activityreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityjoined',
            name='token',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
