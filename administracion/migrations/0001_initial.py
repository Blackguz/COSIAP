# Generated by Django 4.1.7 on 2023-06-13 01:51


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsuariosBaneados',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('curp', models.CharField(max_length=18)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hora', models.TimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Usuario Baneado',
                'verbose_name_plural': 'Usuarios Baneados',
                'db_table': 'usuarios_baneados',
            },
        ),
    ]
