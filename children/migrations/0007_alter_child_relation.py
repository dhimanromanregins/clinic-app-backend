# Generated by Django 5.1.1 on 2024-11-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0006_child_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='relation',
            field=models.CharField(blank=True, choices=[('MOTHER', 'Mother'), ('FATHER', 'Father'), ('AUNTY', 'Aunty'), ('UNCLE', 'Uncle'), ('FRIEND', 'Friend')], max_length=10, null=True),
        ),
    ]
