# Generated by Django 4.1.7 on 2023-04-23 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modalidad',
            name='estatus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='convocatorias.estatus'),
        ),
    ]