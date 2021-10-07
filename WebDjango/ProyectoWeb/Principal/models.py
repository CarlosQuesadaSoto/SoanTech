# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AltaIncidencia(models.Model):
    numero_alta = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    estado = models.IntegerField()
    codigo = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='codigo')
    iderror = models.ForeignKey('Errores', models.DO_NOTHING,db_column='iderror')
    serial_number = models.ForeignKey('Dispositivos', models.DO_NOTHING, db_column='serial_number')


class Departamentos(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=20)


class Dispositivos(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=20)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    marca = models.CharField(max_length=20, blank=True, null=True)
    modelo = models.CharField(max_length=20, blank=True, null=True)
    id_departamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='id_departamento')


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()



class Errores(models.Model):
    iderror = models.IntegerField(primary_key=True)
    tipo_error = models.CharField(max_length=25)
    clase_error = models.CharField(max_length=8)
    prioridad = models.IntegerField()


class SolucionIncidencia(models.Model):
    numero_solucion = models.AutoField(primary_key=True)
    valoracion = models.IntegerField(null=True)
    fecha_fin = models.DateField()
    tecnico = models.CharField(max_length=5)
    numero_alta = models.ForeignKey(AltaIncidencia, models.DO_NOTHING, db_column='numero_alta')


class Usuarios(models.Model):
    codigo = models.CharField(primary_key=True, max_length=5)
    correo = models.CharField(unique=True, max_length=50)
    nombre = models.CharField(max_length=15)
    apellidos = models.CharField(max_length=25)
    password = models.CharField(max_length=10)
    tipo_usuario = models.IntegerField()

