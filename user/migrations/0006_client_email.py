# Generated by Django 3.1.7 on 2021-05-21 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210501_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.BooleanField(default=True),
        ),
    ]
