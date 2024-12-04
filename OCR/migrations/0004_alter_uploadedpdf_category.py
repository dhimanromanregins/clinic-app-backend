# Generated by Django 5.1.1 on 2024-12-04 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OCR', '0003_uploadedpdf_category_alter_uploadedpdf_urn_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedpdf',
            name='category',
            field=models.CharField(choices=[('medical_report', 'Medical Report'), ('sick_leave', 'Sick Leave'), ('parent_sick_leave', 'Parent Sick Leave'), ('prescription', 'Prescription'), ('lab_report', 'Lab Report'), ('To_whome_may_concern', 'To Whome May Concern')], default='medical_report', max_length=20),
        ),
    ]