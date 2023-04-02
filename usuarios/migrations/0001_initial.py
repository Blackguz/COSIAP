# Generated by Django 4.1.7 on 2023-04-01 07:24

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('apellido_materno', models.CharField(max_length=30)),
                ('apellido_paterno', models.CharField(max_length=30)),
                ('telefono_celular', models.CharField(max_length=20)),
                ('nivel_acceso', models.CharField(choices=[('N1', 'Nivel 1'), ('N2', 'Nivel 2'), ('N3', 'Nivel 3')], max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Administradores',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Solicitante',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('apellido_materno', models.CharField(max_length=30)),
                ('apellido_paterno', models.CharField(max_length=30)),
                ('telefono_particular', models.CharField(max_length=20)),
                ('telefono_celular', models.CharField(max_length=20)),
                ('genero', models.CharField(max_length=10)),
                ('ultimo_grado_estudios', models.CharField(max_length=20)),
                ('institucion', models.CharField(max_length=100)),
                ('domicilio_calle', models.CharField(max_length=100)),
                ('domicilio_numero_exterior', models.CharField(max_length=10)),
                ('domicilio_numero_interior', models.CharField(blank=True, max_length=10, null=True)),
                ('domicilio_codigo_postal', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name_plural': 'Solicitantes',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
