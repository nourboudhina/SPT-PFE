# Generated by Django 5.0.4 on 2024-05-07 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(max_length=1000000, primary_key=True, serialize=False, unique=True),
        ),
    ]
