# Generated by Django 4.1.7 on 2023-04-06 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitante',
            name='genero',
            field=models.CharField(max_length=1),
        ),
    ]
