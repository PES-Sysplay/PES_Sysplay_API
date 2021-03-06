# Generated by Django 3.1.7 on 2021-03-20 15:02

import activity.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('photo', models.FileField(null=True, upload_to='activity', validators=[activity.validators.validate_file_extension])),
                ('start_time', models.TimeField()),
                ('start_date', models.DateField()),
                ('duration', models.FloatField()),
                ('normal_price', models.FloatField()),
                ('member_price', models.FloatField(null=True)),
                ('number_participants', models.IntegerField()),
                ('status', models.CharField(choices=[('P', 'Pendiente'), ('C', 'Cancelada'), ('D', 'Finalizada')], max_length=20)),
                ('location', models.CharField(max_length=20)),
                ('only_member', models.BooleanField(default=False)),
                ('activity_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='activity.activitytype')),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'unique_together': {('activity_type', 'start_time', 'location')},
            },
        ),
    ]
