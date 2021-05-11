# Generated by Django 3.1.7 on 2021-05-11 15:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_action', '0006_auto_20210508_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityreview',
            name='stars',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]