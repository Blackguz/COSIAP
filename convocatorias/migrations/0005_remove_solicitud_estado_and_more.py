# Generated by Django 4.1.7 on 2023-06-09 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0004_remove_solicitud_documentos_documentosolicitud'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='estado',
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]