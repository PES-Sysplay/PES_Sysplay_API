# Generated by Django 3.1.7 on 2021-04-06 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20210320_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructedBy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
