# Generated by Django 4.1 on 2024-12-15 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelterapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='img',
            field=models.ImageField(upload_to='pics'),
        ),
    ]
