# Generated by Django 5.1.1 on 2024-09-26 11:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('children', '__first__'),
        ('doctors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_start', models.TimeField()),
                ('slot_end', models.TimeField()),
                ('date', models.DateField()),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childern', to='children.child')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='doctors.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='use', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('doctor', 'slot_start', 'slot_end', 'date')},
            },
        ),
    ]
