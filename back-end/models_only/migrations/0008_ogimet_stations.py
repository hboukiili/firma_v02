# Generated by Django 4.2.1 on 2024-04-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_only', '0007_station_remote_sensing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ogimet_stations',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('lat', models.CharField(max_length=50)),
                ('long', models.CharField(max_length=50)),
                ('location_name', models.CharField(max_length=50)),
            ],
        ),
    ]