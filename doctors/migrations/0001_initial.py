# Generated by Django 5.1.1 on 2024-09-26 11:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayOfWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('specialty', models.CharField(max_length=255)),
                ('experience', models.CharField(max_length=255)),
                ('about', models.TextField()),
                ('hospital_name', models.CharField(max_length=255)),
                ('education', models.CharField(max_length=255)),
                ('registration_id', models.CharField(max_length=255)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='doctors_images/')),
                ('digital_consult', models.BooleanField(default=False)),
                ('hospital_visit', models.BooleanField(default=False)),
                ('price', models.BigIntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('languages', models.ManyToManyField(related_name='doctors', to='doctors.language')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='doctors.location')),
            ],
        ),
        migrations.CreateModel(
            name='WorkingPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('morning_start', models.TimeField(blank=True, null=True)),
                ('morning_end', models.TimeField(blank=True, null=True)),
                ('afternoon_start', models.TimeField(blank=True, null=True)),
                ('afternoon_end', models.TimeField(blank=True, null=True)),
                ('day_of_week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_periods', to='doctors.dayofweek')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_periods', to='doctors.doctor')),
            ],
        ),
    ]
