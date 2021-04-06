# Generated by Django 3.1.7 on 2021-04-06 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('activity', '0005_instructedby'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='user.organizer'),
        ),
        migrations.AddField(
            model_name='activity',
            name='organized_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='user.organization'),
        ),
        migrations.AddField(
            model_name='instructedby',
            name='activity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='activity.activity'),
        ),
        migrations.AddField(
            model_name='instructedby',
            name='organizer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='user.organizer'),
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together={('activity_type', 'start_date', 'start_time', 'location', 'organized_by')},
        ),
        migrations.AlterUniqueTogether(
            name='instructedby',
            unique_together={('activity', 'organizer')},
        ),
    ]
