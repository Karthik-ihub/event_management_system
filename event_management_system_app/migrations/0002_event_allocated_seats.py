# Generated by Django 5.1.5 on 2025-01-21 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management_system_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allocated_seats',
            field=models.IntegerField(default=0),
        ),
    ]
