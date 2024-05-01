# Generated by Django 5.0.4 on 2024-04-30 19:59

import django.db.models.deletion
from django.db import migrations, models
from django.utils import timezone  

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gouvernorat',
            fields=[
                ('id', models.CharField(max_length=1000000, primary_key=True, serialize=False, unique=True)),
                ('options', models.CharField(choices=[('Ariana', 'Ariana'), ('Béja', 'Béja'), ('Ben Arous', 'Ben Arous'), ('Bizerte', 'Bizerte'), ('Gabès', 'Gabès'), ('Gafsa', 'Gafsa'), ('Jendouba', 'Jendouba'), ('Kairouan', 'Kairouan'), ('Kasserine', 'Kasserine'), ('Kébili', 'Kébili'), ('Le Kef', 'Le Kef'), ('Mahdia', 'Mahdia'), ('La Manouba', 'La Manouba'), ('Médenine', 'Médenine'), ('Monastir', 'Monastir'), ('Nabeul', 'Nabeul'), ('Sfax', 'Sfax'), ('Sidi Bouzid', 'Sidi Bouzid'), ('Siliana', 'Siliana'), ('Sousse', 'Sousse'), ('Tataouine', 'Tataouine'), ('Tozeur', 'Tozeur'), ('Tunis', 'Tunis'), ('Zaghouan', 'Zaghouan')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.CharField(max_length=1000, primary_key=True, serialize=False, unique=True)),
                ('grade', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.CharField(max_length=1000, primary_key=True, serialize=False, unique=True)),
                ('groupe', models.CharField(max_length=100)),
                ('tarif', models.DecimalField(decimal_places=5, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Hopital',
            fields=[
                ('id', models.CharField(max_length=1000, primary_key=True, serialize=False, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Nationalite',
            fields=[
                ('id', models.CharField(max_length=1000, primary_key=True, serialize=False, unique=True)),
                ('nationalite', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='medecin',
            name='addresse',
            field=models.CharField(default=0, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='date_nais',
            field=models.DateField(default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='email',
            field=models.EmailField(default=0, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='fullname',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='image',
            field=models.ImageField(default=0, upload_to='categories/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='phone',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='sexe',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='addresse',
            field=models.CharField(default=0, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='date_naiss',
             field=models.DateField(default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='sexe',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medecin',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='medecin',
            name='username',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(max_length=1000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='medecin',
            name='gouvernorat',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='gouver', to='account.gouvernorat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gouvernorat',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='gouv', to='account.gouvernorat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='grade',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='grade_med', to='account.grade'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='groupe',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='account.groupe'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medecin',
            name='hopitale',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='hopitale_med', to='account.hopital'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_agent', models.CharField(max_length=1000, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=1000)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fullname', models.CharField(max_length=50)),
                ('addresse', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sexe', models.CharField(max_length=5)),
                ('image', models.ImageField(upload_to='categories/')),
                ('date_naiss', models.DateField()),
                ('gouvernorat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gouv_ag', to='account.gouvernorat')),
                ('hopitale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hopitale_ag', to='account.hopital')),
                ('nationalite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nat_ag', to='account.nationalite')),
            ],
        ),
        migrations.AddField(
            model_name='medecin',
            name='nationalite',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='natio', to='account.nationalite'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='nationalite',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='nat', to='account.nationalite'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.CharField(max_length=1000, primary_key=True, serialize=False, unique=True)),
                ('service', models.CharField(max_length=100)),
                ('hopitale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hop', to='account.hopital')),
            ],
        ),
        migrations.AddField(
            model_name='medecin',
            name='service',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='servic', to='account.service'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Specialite',
            fields=[
                ('id', models.CharField(max_length=1000, primary_key=True, serialize=False, unique=True)),
                ('specialite', models.CharField(max_length=100)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serv', to='account.service')),
            ],
        ),
        migrations.AddField(
            model_name='medecin',
            name='sepcialite',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='spec', to='account.specialite'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TokenForAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=5000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='account.agent')),
            ],
        ),
    ]