# Generated by Django 5.0.4 on 2024-05-20 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_room_medecin_room_patient_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
