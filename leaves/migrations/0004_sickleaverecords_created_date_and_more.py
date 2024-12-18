# Generated by Django 5.1.1 on 2024-11-21 06:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0003_sickleaverecords'),
    ]

    operations = [
        migrations.AddField(
            model_name='sickleaverecords',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sickleaverecords',
            name='leave_request_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sickleaverecords',
            name='document',
            field=models.FileField(upload_to='sick_leave_documents/'),
        ),
    ]
