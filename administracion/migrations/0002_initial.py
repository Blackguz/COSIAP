# Generated by Django 4.1.7 on 2023-06-09 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariosbaneados',
            name='usuario',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='usuarios.solicitante'),
        ),
    ]
