# Generated by Django 5.1.1 on 2024-11-26 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0004_doctor_tele_medicine_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='price',
            field=models.BigIntegerField(default=0),
        ),
    ]
