# Generated by Django 5.0.4 on 2024-04-30 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageAcceuil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postwithimage', models.ImageField(upload_to='categories/')),
                ('postwithtet', models.CharField(max_length=1000)),
            ],
        ),
    ]
