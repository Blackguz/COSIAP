# Generated by Django 4.1.7 on 2023-04-05 22:24

import convocatorias.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='documentos',
            field=models.FileField(blank=True, null=True, upload_to=convocatorias.utils.user_directory_path),
        ),
    ]