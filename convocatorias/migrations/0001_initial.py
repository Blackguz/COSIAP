# Generated by Django 4.1.7 on 2023-04-04 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estatus',
            fields=[
                ('id_estatus', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Modalidad',
            fields=[
                ('id_modalidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('presupuesto', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('monto_solicitado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('documentos', models.FilePathField()),
                ('estado', models.CharField(max_length=255)),
                ('monto_aprobado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_solicitud', models.DateField()),
                ('observaciones', models.TextField()),
                ('id_solicitud', models.AutoField(primary_key=True, serialize=False)),
                ('id_estatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.estatus')),
                ('id_modalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.modalidad')),
                ('id_solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.solicitante')),
            ],
        ),
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id_formulario', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(max_length=255)),
                ('id_modalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.modalidad')),
            ],
        ),
        migrations.CreateModel(
            name='AtributosFormulario',
            fields=[
                ('id_atributos_formularios', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('tipo_atributo', models.CharField(max_length=255)),
                ('id_formulario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convocatorias.formulario')),
            ],
        ),
    ]
