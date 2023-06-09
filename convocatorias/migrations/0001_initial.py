# Generated by Django 4.1.7 on 2023-06-13 01:51

import convocatorias.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtributosFormulario',
            fields=[
                ('id_atributos_formularios', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=85)),
                ('tipo_atributo', models.CharField(choices=[('Texto', 'Texto'), ('Numero', 'Numero'), ('Fecha', 'Fecha'), ('Documento', 'Documento'), ('Telefono', 'Telefono')], max_length=15)),
                ('es_documento', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.FileField(upload_to=convocatorias.models.solicitud_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Estatus',
            fields=[
                ('id_estatus', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id_formulario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(default='sin nombre', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Modalidad',
            fields=[
                ('id_modalidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('requisitos', models.TextField(blank=True, default='sin requisitos', null=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('presupuesto', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('monto_solicitado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monto_aprobado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_solicitud', models.DateField()),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('id_solicitud', models.AutoField(primary_key=True, serialize=False)),
                ('id_estatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.estatus')),
                ('id_modalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.modalidad')),
            ],
        ),
    ]
