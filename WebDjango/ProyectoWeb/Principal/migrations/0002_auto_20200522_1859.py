# Generated by Django 2.2.3 on 2020-05-22 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Principal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solucionincidencia',
            name='valoracion',
            field=models.IntegerField(null=True),
        ),
    ]