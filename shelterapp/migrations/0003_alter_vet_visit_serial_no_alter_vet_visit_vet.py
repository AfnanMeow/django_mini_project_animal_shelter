# Generated by Django 4.1 on 2024-12-29 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shelterapp', '0002_alter_pet_adoption_date_alter_pet_adoption_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vet_visit',
            name='serial_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='shelterapp.pet', to_field='serial_no'),
        ),
        migrations.AlterField(
            model_name='vet_visit',
            name='vet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vet_visits', to='shelterapp.vet', to_field='nid'),
        ),
    ]
