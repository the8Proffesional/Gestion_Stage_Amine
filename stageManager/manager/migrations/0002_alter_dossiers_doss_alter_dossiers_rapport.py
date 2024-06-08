# Generated by Django 5.0.6 on 2024-06-08 00:16

import manager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossiers',
            name='Doss',
            field=models.FileField(upload_to=manager.models.pdf2_upload_to),
        ),
        migrations.AlterField(
            model_name='dossiers',
            name='Rapport',
            field=models.FileField(upload_to=manager.models.pdf1_upload_to),
        ),
    ]