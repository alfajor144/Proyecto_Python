# Generated by Django 3.1.1 on 2020-09-28 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id_oferta', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200, verbose_name='Titulo')),
                ('descripcion', models.TextField()),
                ('pais', models.CharField(max_length=50, verbose_name='pais')),
                ('fecha_inicio', models.DateField(verbose_name='fecha inicio')),
                ('fecha_final', models.DateField(verbose_name='fecha final')),
                ('link', models.CharField(max_length=2050, verbose_name='link')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200, verbose_name='nombre')),
                ('apellido', models.CharField(max_length=200, verbose_name='apellido')),
                ('contrasenia', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cv', models.CharField(blank=True, max_length=300, null=True)),
                ('isAdmin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Postulacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.IntegerField(blank=True, null=True)),
                ('fecha_uno', models.DateField(blank=True, null=True, verbose_name='fecha uno')),
                ('fecha_dos', models.DateField(blank=True, null=True, verbose_name='fecha dos')),
                ('fecha_tres', models.DateField(blank=True, null=True, verbose_name='fecha tres')),
                ('id_oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.oferta')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='oferta',
            name='Usuario_id',
            field=models.ManyToManyField(related_name='Postulacion', through='Usuario.Postulacion', to='Usuario.Usuario'),
        ),
        migrations.CreateModel(
            name='masBuscados',
            fields=[
                ('id_buscado', models.AutoField(primary_key=True, serialize=False)),
                ('puesto', models.IntegerField()),
                ('id_Oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.oferta')),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('id_Oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.oferta')),
            ],
        ),
    ]
