# Generated by Django 5.1.1 on 2024-10-01 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0002_leaves_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaves',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
