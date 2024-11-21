# Generated by Django 5.1.1 on 2024-11-21 05:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0007_alter_child_relation'),
        ('leaves', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SickLeaveRequestView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.CharField(max_length=255)),
                ('sender', models.CharField(max_length=255)),
                ('children', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='children.child')),
            ],
        ),
    ]
