# Generated by Django 5.1.1 on 2024-11-20 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0002_alter_child_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='child',
            name='profile_picture',
        ),
    ]
