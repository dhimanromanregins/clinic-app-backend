# Generated by Django 5.1.1 on 2024-11-25 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='devive_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
