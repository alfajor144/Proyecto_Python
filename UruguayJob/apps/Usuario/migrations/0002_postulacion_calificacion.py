# Generated by Django 3.1.1 on 2020-09-27 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postulacion',
            name='calificacion',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
