# Generated by Django 5.1.1 on 2024-12-02 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0007_alter_child_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='category',
            field=models.CharField(choices=[('medical_report', 'Medical Report'), ('sick_leave', 'Sick Leave'), ('parent_sick_leave', 'Parent Sick Leave'), ('prescription', 'Prescription'), ('lab_report', 'Lab Report')], default='medical_report', max_length=20),
        ),
    ]
