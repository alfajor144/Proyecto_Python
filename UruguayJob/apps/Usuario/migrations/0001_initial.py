# Generated by Django 3.1.1 on 2020-10-20 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuscoJob',
            fields=[
                ('nro_llamado', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField(max_length=100, verbose_name='fecha_inicio')),
                ('fecha_fin', models.DateField(max_length=100, verbose_name='fecha_fin')),
                ('titulo', models.CharField(max_length=100, verbose_name='titulo')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('empresa_nombre', models.CharField(max_length=100, verbose_name='empresa_nombre')),
                ('lugar', models.CharField(max_length=100, verbose_name='lugar')),
                ('jornada_laboral', models.CharField(max_length=100, verbose_name='jornada_laboral')),
                ('puestos_vacantes', models.CharField(max_length=100, verbose_name='puestos_vacantes')),
                ('categoria', models.CharField(max_length=100, verbose_name='categoria')),
                ('subCategoria', models.CharField(max_length=100, verbose_name='subCategoria')),
                ('requisitos', models.CharField(max_length=100, verbose_name='requisitos')),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaBJ',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaUC',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id_oferta', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200, verbose_name='Titulo')),
                ('descripcion', models.TextField()),
                ('pais', models.CharField(max_length=50, verbose_name='pais')),
                ('fecha_inicio', models.DateField(verbose_name='fecha inicio')),
                ('fecha_final', models.DateField(verbose_name='fecha final')),
                ('CategoriaUC', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuario.categoriauc')),
            ],
        ),
        migrations.CreateModel(
            name='UruguayConcursa',
            fields=[
                ('nro_llamado', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100, verbose_name='titulo')),
                ('fecha_inicio', models.DateField(max_length=100, verbose_name='fecha_inicio')),
                ('fecha_fin', models.DateField(max_length=100, verbose_name='fecha_fin')),
                ('tipo_tarea', models.CharField(max_length=100, verbose_name='tipo_tarea')),
                ('tipo_vinculo', models.CharField(max_length=100, verbose_name='tipo_vinculo')),
                ('tiempo_contrato', models.CharField(max_length=100, verbose_name='tiempo_contrato')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('requisitos', models.TextField(blank=True, null=True)),
                ('recepcion_postulaciones', models.TextField(blank=True, null=True)),
                ('recepcion_consultas', models.TextField(blank=True, null=True)),
                ('telefono_consultas', models.CharField(max_length=100, verbose_name='telefono_consultas')),
                ('organismo', models.CharField(max_length=100, verbose_name='organismo')),
                ('comentario_interes', models.TextField(blank=True, null=True)),
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
            name='SubCategoriaBJ',
            fields=[
                ('id_Sub', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('CategoriaUC', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuario.categoriabj')),
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
                ('fecha_Definitiva', models.DateField(blank=True, null=True, verbose_name='Definitiva')),
                ('comentario', models.TextField(blank=True, null=True)),
                ('id_oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.oferta')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='oferta',
            name='SubCategoriaBJ',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuario.subcategoriabj'),
        ),
        migrations.AddField(
            model_name='oferta',
            name='Usuario_id',
            field=models.ManyToManyField(related_name='Postulacion', through='Usuario.Postulacion', to='Usuario.Usuario'),
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id_c', models.AutoField(primary_key=True, serialize=False)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True, verbose_name='direccion')),
                ('telefono', models.CharField(blank=True, max_length=10, null=True, verbose_name='telefono')),
                ('ci', models.CharField(blank=True, max_length=10, null=True, verbose_name='telefono')),
                ('experiencia', models.TextField(blank=True, null=True)),
                ('formacion', models.TextField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='updateFoto/')),
                ('idUsu', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Usuario.usuario')),
            ],
        ),
    ]
