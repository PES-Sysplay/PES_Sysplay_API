# Generated by Django 3.1.7 on 2021-05-21 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_blocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='super_host',
        ),
    ]
