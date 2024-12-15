# Generated by Django 4.1 on 2024-12-15 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('img', models.CharField(default=' ', max_length=355)),
                ('type', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('estimated_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('adopter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adopted_pets', to='accounts.adopter', to_field='user_id', unique=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donated_pets', to='accounts.donor', to_field='user_id', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('reason', models.TextField()),
                ('serial_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='shelterapp.pet', to_field='serial_no', unique=True)),
                ('vet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vet_visits', to='shelterapp.vet', to_field='email', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TakenCare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_nid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cared_pets', to='accounts.authority', to_field='user_id')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='care_takers', to='shelterapp.pet', to_field='serial_no')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicines', models.TextField()),
                ('vet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='shelterapp.vet', to_field='email', unique=True)),
            ],
        ),
    ]
