# Generated by Django 5.1.1 on 2024-11-26 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_notifications_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='tele_medicine_doctor',
            field=models.BooleanField(default=False),
        ),
    ]
