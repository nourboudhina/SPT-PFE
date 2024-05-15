# Generated by Django 5.0.4 on 2024-05-06 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_gouvernorat_alter_user_nationalite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_naiss',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='nationalite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nat', to='account.nationalite'),
        ),
    ]