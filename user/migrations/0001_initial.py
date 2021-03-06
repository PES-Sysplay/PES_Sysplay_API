# Generated by Django 3.1.7 on 2021-04-06 19:14

import activity.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('super_host', models.BooleanField(default=False)),
                ('photo', models.FileField(null=True, upload_to='user', validators=[activity.validators.validate_file_extension])),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='auth.user')),
                ('admin', models.BooleanField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.organization')),
            ],
        ),
    ]
