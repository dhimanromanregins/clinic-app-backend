# Generated by Django 5.1.1 on 2024-11-20 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
