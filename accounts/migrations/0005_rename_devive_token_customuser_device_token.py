# Generated by Django 5.1.1 on 2024-11-25 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_devive_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='devive_token',
            new_name='device_token',
        ),
    ]
