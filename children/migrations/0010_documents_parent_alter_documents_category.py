# Generated by Django 5.1.1 on 2024-12-04 09:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0009_alter_child_uae_number_alter_child_child_id_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documents',
            name='category',
            field=models.CharField(choices=[('medical_report', 'Medical Report'), ('sick_leave', 'Sick Leave'), ('parent_sick_leave', 'Parent Sick Leave'), ('prescription', 'Prescription'), ('lab_report', 'Lab Report'), ('To_whome_may_concern', 'To Whome May Concern')], default='medical_report', max_length=20),
        ),
    ]
