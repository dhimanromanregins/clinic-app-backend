# Generated by Django 5.1.1 on 2024-12-02 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_customuser_tele_medicine_doctor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='body',
            new_name='body',
        ),
    ]
