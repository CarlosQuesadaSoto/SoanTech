
from rest_framework.response import Response
from rest_framework.views import APIView

from Principal.models import *
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.views.generic import View
from datetime import datetime, timedelta, date
from django.conf import settings
from django.core.mail import send_mail


def log(request):
    return render(request, "log.html")
def inicio(request):
    return render(request, "inicio.html")

def informacion(request):
    return render(request, "informacion.html")

def login(request):
    if request.user.is_authenticated:
        return render(request, "inicio.html")
    else:
        return render(request, "log.html")
#Superusuario = admin, root
def takelogindata(request):
    if request.GET["correo"] and request.GET["pass"]:
        correo=request.GET["correo"]
        password=request.GET["pass"]
        user = authenticate(username=correo, password=password)
        if request.user.is_authenticated:
            usuario = Usuarios.objects.filter(correo=correo).first()
            codigo = usuario.codigo
            print(codigo)
            request.session['codigo'] = codigo
        else:
            if user is not None:
                do_login(request, user)
                usuario = Usuarios.objects.filter(correo=correo).first()
                codigo = usuario.codigo
                print(codigo)
                request.session['codigo'] = codigo
                return render(request, "inicio.html")
            else:
                return render(request, "logempty.html")
    else:
        return render(request,"logempty.html")

def cuenta(request):
    if request.user.is_authenticated:
        name=request.user.get_username()
        return render(request,"logout.html", {"usuario":name})
    else:
        return render(request, "log.html")

def cuentaout(request):
    do_logout(request)
    return render(request, "inicio.html")


def estadisticas(request):
    if request.user.is_authenticated:
        name=request.user.get_username()
        return render(request,"estadisticas.html", {"usuario":name})
    else:
        return render(request, "log.html")

def getdata():
    data = {}
    return JsonResponse(data)

def getdataSemana():
    data = {}
    return JsonResponse(data)

class ChartsData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        #Primer gráfico
        noresueltas1 = AltaIncidencia.objects.filter(estado=1).count()
        noresueltas2 = AltaIncidencia.objects.filter(estado=2).count()
        noresueltas = noresueltas1 + noresueltas2
        siresueltas = SolucionIncidencia.objects.all().count()
        iniciadas = AltaIncidencia.objects.filter(estado=1).count()
        proceso = AltaIncidencia.objects.filter(estado=2).count()
        finalizadas = SolucionIncidencia.objects.all().count()
        total = noresueltas + siresueltas
        #Segundo gráfico
        mal=SolucionIncidencia.objects.filter(valoracion=1).count()
        regular= SolucionIncidencia.objects.filter(valoracion=2).count()
        bien = SolucionIncidencia.objects.filter(valoracion=3).count()
        muybien = SolucionIncidencia.objects.filter(valoracion=4).count()
        excelente = SolucionIncidencia.objects.filter(valoracion=5).count()
        media=(mal+regular+bien+muybien+excelente)/5
        #Paso de información a las gráficas
        labels = ['Resueltas', 'No Resueltas', 'Iniciada', 'En Proceso', 'Finalizadas', 'Total']
        labels2 = ['Mal', 'Regular', 'Bien', 'Muy Bien', 'Excelente', 'Media']
        default_items = [siresueltas, noresueltas,iniciadas,proceso,finalizadas,total]
        default_items2 = [mal, regular, bien, muybien, excelente, media]
        data = {
            "labels": labels,
            "labels2":labels2,
            "default": default_items,
            "default2": default_items2,
        }
        return Response(data)

## GRAFICA DE ULTIMA SEMANA
class UltimaSemana(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        fecha = datetime.now().date()
        #Primer gráfico
        noresueltas1 = AltaIncidencia.objects.filter(estado=1, fecha_inicio__gte=fecha-timedelta(days=7), fecha_inicio__lte=fecha).count()
        noresueltas2 = AltaIncidencia.objects.filter(estado=2, fecha_inicio__gte=fecha-timedelta(days=7), fecha_inicio__lte=fecha).count()
        noresueltas = noresueltas1 + noresueltas2
        siresueltas = SolucionIncidencia.objects.filter(fecha_fin__gte=fecha-timedelta(days=7), fecha_fin__lte=fecha).count()
        iniciadas = AltaIncidencia.objects.filter(estado=1,fecha_inicio__gte=fecha-timedelta(days=7), fecha_inicio__lte=fecha).count()
        proceso = AltaIncidencia.objects.filter(estado=2,fecha_inicio__gte=fecha-timedelta(days=7), fecha_inicio__lte=fecha).count()
        finalizadas = SolucionIncidencia.objects.filter(fecha_fin__gte=fecha-timedelta(days=7), fecha_fin__lte=fecha).count()
        total = noresueltas + siresueltas
        #Segundo gráfico
        mal=SolucionIncidencia.objects.filter(valoracion=1, fecha_fin__gte=fecha-timedelta(days=7), fecha_fin__lte=fecha).count()
        regular= SolucionIncidencia.objects.filter(valoracion=2, fecha_fin__gte=fecha-timedelta(days=7), fecha_fin__lte=fecha).count()
        bien = SolucionIncidencia.objects.filter(valoracion=3, fecha_fin__gte=fecha-timedelta(days=7), fecha_fin__lte=fecha).count()
        muybien = SolucionIncidencia.objects.filter(valoracion=4, fecha_fin__gte=fecha-timedelta(days=7), fecha_fin__lte=fecha).count()
        excelente = SolucionIncidencia.objects.filter(valoracion=5, fecha_fin__gte=fecha-timedelta(days=7), fecha_fin__lte=fecha).count()
        media=(mal+regular+bien+muybien+excelente)/5
        #Paso de información a las gráficas
        labels = ['Resueltas', 'No Resueltas', 'Iniciada', 'En Proceso', 'Finalizadas', 'Total']
        labels2 = ['Mal', 'Regular', 'Bien', 'Muy Bien', 'Excelente', 'Media']
        default_items = [siresueltas, noresueltas,iniciadas,proceso,finalizadas,total]
        default_items2 = [mal, regular, bien, muybien, excelente, media]
        data = {
            "labels": labels,
            "labels2":labels2,
            "default": default_items,
            "default2": default_items2,
        }
        return Response(data)

## GRAFICA DE ULTIMO AÑO
class UltimoAno(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        fecha = datetime.now().date()
        #Primer gráfico
        noresueltas1 = AltaIncidencia.objects.filter(estado=1, fecha_inicio__gte=fecha-timedelta(days=30), fecha_inicio__lte=fecha).count()
        noresueltas2 = AltaIncidencia.objects.filter(estado=2, fecha_inicio__gte=fecha-timedelta(days=30), fecha_inicio__lte=fecha).count()
        noresueltas = noresueltas1 + noresueltas2
        siresueltas = SolucionIncidencia.objects.filter(fecha_fin__gte=fecha-timedelta(days=30), fecha_fin__lte=fecha).count()
        iniciadas = AltaIncidencia.objects.filter(estado=1,fecha_inicio__gte=fecha-timedelta(days=30), fecha_inicio__lte=fecha).count()
        proceso = AltaIncidencia.objects.filter(estado=2,fecha_inicio__gte=fecha-timedelta(days=30), fecha_inicio__lte=fecha).count()
        finalizadas = SolucionIncidencia.objects.filter(fecha_fin__gte=fecha-timedelta(days=30), fecha_fin__lte=fecha).count()
        total = noresueltas + siresueltas
        #Segundo gráfico
        mal=SolucionIncidencia.objects.filter(valoracion=1, fecha_fin__gte=fecha-timedelta(days=30), fecha_fin__lte=fecha).count()
        regular= SolucionIncidencia.objects.filter(valoracion=2, fecha_fin__gte=fecha-timedelta(days=30), fecha_fin__lte=fecha).count()
        bien = SolucionIncidencia.objects.filter(valoracion=3, fecha_fin__gte=fecha-timedelta(days=30), fecha_fin__lte=fecha).count()
        muybien = SolucionIncidencia.objects.filter(valoracion=4, fecha_fin__gte=fecha-timedelta(days=30), fecha_fin__lte=fecha).count()
        excelente = SolucionIncidencia.objects.filter(valoracion=5, fecha_fin__gte=fecha-timedelta(days=30), fecha_fin__lte=fecha).count()
        media=(mal+regular+bien+muybien+excelente)/5
        #Paso de información a las gráficas
        labels = ['Resueltas', 'No Resueltas', 'Iniciada', 'En Proceso', 'Finalizadas', 'Total']
        labels2 = ['Mal', 'Regular', 'Bien', 'Muy Bien', 'Excelente', 'Media']
        default_items = [siresueltas, noresueltas,iniciadas,proceso,finalizadas,total]
        default_items2 = [mal, regular, bien, muybien, excelente, media]
        data = {
            "labels": labels,
            "labels2":labels2,
            "default": default_items,
            "default2": default_items2,
        }
        return Response(data)

## GRAFICA DE ULTIMO AÑO
class UltimoMes(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        fecha = datetime.now().date()
        #Primer gráfico
        noresueltas1 = AltaIncidencia.objects.filter(estado=1, fecha_inicio__gte=fecha-timedelta(days=365), fecha_inicio__lte=fecha).count()
        noresueltas2 = AltaIncidencia.objects.filter(estado=2, fecha_inicio__gte=fecha-timedelta(days=365), fecha_inicio__lte=fecha).count()
        noresueltas = noresueltas1 + noresueltas2
        siresueltas = SolucionIncidencia.objects.filter(fecha_fin__gte=fecha-timedelta(days=365), fecha_fin__lte=fecha).count()
        iniciadas = AltaIncidencia.objects.filter(estado=1,fecha_inicio__gte=fecha-timedelta(days=365), fecha_inicio__lte=fecha).count()
        proceso = AltaIncidencia.objects.filter(estado=2,fecha_inicio__gte=fecha-timedelta(days=365), fecha_inicio__lte=fecha).count()
        finalizadas = SolucionIncidencia.objects.filter(fecha_fin__gte=fecha-timedelta(days=365), fecha_fin__lte=fecha).count()
        total = noresueltas + siresueltas
        #Segundo gráfico
        mal=SolucionIncidencia.objects.filter(valoracion=1, fecha_fin__gte=fecha-timedelta(days=365), fecha_fin__lte=fecha).count()
        regular= SolucionIncidencia.objects.filter(valoracion=2, fecha_fin__gte=fecha-timedelta(days=365), fecha_fin__lte=fecha).count()
        bien = SolucionIncidencia.objects.filter(valoracion=3, fecha_fin__gte=fecha-timedelta(days=365), fecha_fin__lte=fecha).count()
        muybien = SolucionIncidencia.objects.filter(valoracion=4, fecha_fin__gte=fecha-timedelta(days=365), fecha_fin__lte=fecha).count()
        excelente = SolucionIncidencia.objects.filter(valoracion=5, fecha_fin__gte=fecha-timedelta(days=365), fecha_fin__lte=fecha).count()
        media=(mal+regular+bien+muybien+excelente)/5
        #Paso de información a las gráficas
        labels = ['Resueltas', 'No Resueltas', 'Iniciada', 'En Proceso', 'Finalizadas', 'Total']
        labels2 = ['Mal', 'Regular', 'Bien', 'Muy Bien', 'Excelente', 'Media']
        default_items = [siresueltas, noresueltas,iniciadas,proceso,finalizadas,total]
        default_items2 = [mal, regular, bien, muybien, excelente, media]
        data = {
            "labels": labels,
            "labels2":labels2,
            "default": default_items,
            "default2": default_items2,
        }
        return Response(data)

def filtrarstats(request):
    if request.user.is_authenticated:
        fecha=request.GET["fecha"]
        if fecha == "TODAS":
            return render(request, "estadisticas.html")
        elif fecha == "ÚLTIMO AÑO":
            return render(request,"ultimoAno.html")
        elif fecha == "ÚLTIMO MES":
            return render(request,"ultimoMes.html")
        elif fecha == "ÚLTIMA SEMANA":
            return render(request,"ultimaSemana.html")
    else:
        return render(request, "log.html")

def dispositivos(request):
    if request.user.is_authenticated:
        dispositivo = Dispositivos.objects.all()
        return render(request, "dispositivos.html", {"dispositivo": dispositivo})
    else:
        return render(request, "log.html")

def usuarios(request):
    if request.user.is_authenticated:
        usuario = Usuarios.objects.all()
        user = Departamentos.objects.all()
        return render(request, "usuarios.html", {"usuario": usuario, "user": user})
    else:
        return render(request, "log.html")

## FILTRADO Y MODIFICACION (ALTA, BAJA Y MODIFICACION DE USUARIOS)

def filtrarUsuarios(request):
    if request.user.is_authenticated:
        tipo = request.GET["tipo"]
        if tipo=="TODOS":
            usuario=Usuarios.objects.all()
            depar = Departamentos.objects.all()
            return render(request, "usuarios.html", {"usuario": usuario})
        else:
            dispositivo=Dispositivos.objects.filter(tipo=tipo)
            depar = Departamentos.objects.all()
            return render(request, "dispositivos.html", {"dispositivo": dispositivo, "departamento": depar})
    else:
        return render(request, "log.html")

def altaUser(request):
    return render(request,"altaUsuario.html")
def altaUserData(request):
    if request.GET["nombre"] and request.GET["apellidos"] and request.GET["correo"] and request.GET["codigo"] and request.GET["password"]:
        nombre=request.GET["nombre"]
        apellidos=request.GET["apellidos"]
        correo = request.GET["correo"]
        code = request.GET["codigo"]
        tipoUsuario = 2
        passUser = request.GET["password"]
        u = Usuarios.objects.filter(codigo=code)
        u.exists()
        if not u:
            user = Usuarios(code, correo, nombre,apellidos,passUser,tipoUsuario)
            user.save()
            return render(request, "endUser.html")
        else:
            mensaje="El Código de operador introducido ya existe."
            return render(request, "altaEmptyUser.html",{"mensaje":mensaje})

    else:
        mensaje="Por favor, rellene todos los campos antes de registrar el Usuario."
        return render(request, "altaEmptyUser.html",{"mensaje":mensaje})
def modUser(request):
    return render(request,"modificarUsuarioSearch.html")
def modUserSearch(request):
    if request.GET["codigo"]:
        code = request.GET["codigo"]
        u = Usuarios.objects.filter(codigo=code)
        u.exists()
        if u:
            u = Usuarios.objects.get(codigo=code)
            name = u.nombre
            correo = u.correo
            apellidos = u.apellidos
            password = u.password
            return render(request, "modificarUsuario.html",{"nombre":name,"correo":correo,"apellidos":apellidos,"pass":password,"code":code})
        else:
            mensaje = "El Código de operador introducido no existe."
            return render(request, "modificarUsuarioSearchEmpty.html", {"mensaje": mensaje})

    else:
        mensaje = "Por favor, rellene todos los campos antes de registrar el Usuario."
        return render(request, "modificarUsuarioSearchEmpty.html", {"mensaje": mensaje})
def modUserData(request):
    if request.GET["nombre"] and request.GET["apellidos"] and request.GET["correo"] and request.GET["codigo"] and request.GET["password"]:
        nombre = request.GET["nombre"]
        apellidos = request.GET["apellidos"]
        correo = request.GET["correo"]
        code = request.GET["codigo"]
        tipoUsuario = 2
        passUser = request.GET["password"]
        u = Usuarios.objects.filter(codigo=code)
        u.exists()
        if u:
            user = Usuarios(code, correo, nombre, apellidos, passUser, tipoUsuario)
            user.save()
            return render(request, "endUser.html")
        else:
            mensaje = "El Código de operador introducido no existe."
            return render(request, "modificarEmptyUsuario.html", {"mensaje": mensaje})

    else:
        mensaje = "Por favor, rellene todos los campos antes de registrar el Usuario."
        return render(request, "modificarEmptyUsuario.html", {"mensaje": mensaje})
def eliminarUser(request):
    return render(request,"eliminarUsuario.html")
def eliminarUserData(request):
    if request.GET["codigo"]:
        code=request.GET["codigo"]
        p = Usuarios.objects.filter(codigo=code)
        if p:
            request.session['codigo'] = code  # asi podemos pasar variables entre vistas
            d = Usuarios.objects.get(codigo=code)
            return render(request, "eliminarusuconfirm.html",{"usuario":d})
        else:
            mensaje = "El código de operario introducido no existe."
            return render(request, "eliminarEmptyUsuarios.html", {"mensaje": mensaje})
    else:
        mensaje = "Por favor, rellene todos los campos antes de registrar el Usuario."
        return render(request, "eliminarEmptyUsuarios.html", {"mensaje": mensaje})

def bajauserconfirm(request):
    eleccion = request.GET["choose"]
    if eleccion == "Eliminar":
        codigo = request.session.get('codigo')  # asi podemos recoger variables entre vistas
        d = Usuarios.objects.get(codigo=codigo)
        d.delete()
        return render(request, "endUser.html")
    elif eleccion == "Cancelar":
        return render(request, "eliminarUsuario.html")
def altaSuperUser(request):
    return render(request,"altaSuperUsuario.html")
def altaSuperUserData(request):
    if request.GET["nombre"] and request.GET["apellidos"] and request.GET["correo"] and request.GET["codigo"] and request.GET["password"]:
        nombre=request.GET["nombre"]
        apellidos=request.GET["apellidos"]
        correo = request.GET["correo"]
        code = request.GET["codigo"]
        tipoUsuario = 1
        passUser = request.GET["password"]
        u = Usuarios.objects.filter(codigo=code)
        u.exists()
        if not u:
            userbbdd = Usuarios(code, correo, nombre, apellidos, passUser, tipoUsuario)
            userbbdd.save()
            user = User.objects.create_superuser(correo,correo,passUser)
            user.last_name = apellidos
            user.save()
            return render(request,"endSuperUser.html")
        else:
            mensaje="El Código de operador introducido ya existe."
            return render(request,"altaEmptySuperUser.html",{"mensaje":mensaje})

    else:
        mensaje="Por favor, rellene todos los campos antes de registrar el Administrador."
        return render(request, "altaEmptySuperUser.html",{"mensaje":mensaje})

def modSuperUser(request):
    return render(request,"SuperUserSearch.html")
def modSuperUserSearch(request):
    if request.GET["correo"]:
        correo = request.GET["correo"]
        u = Usuarios.objects.filter(correo=correo, tipo_usuario=1)
        u.exists()
        if u:
            u = Usuarios.objects.get(correo=correo)
            name = u.nombre
            code = u.codigo
            apellidos = u.apellidos
            password = u.password
            return render(request, "modSuperUser.html",{"nombre": name, "correo": correo, "apellidos": apellidos, "pass": password, "code": code})
        else:
            mensaje="El correo de administrador introducido no existe."
            return render(request,"SuperUserSearchEmpty.html",{"mensaje":mensaje})
    else:
        mensaje="Por favor, rellene todos los campos antes de modificar el Administrador."
        return render(request, "SuperUserSearchEmpty.html",{"mensaje":mensaje})
def modSuperUserData(request):
    if request.GET["nombre"] and request.GET["apellidos"] and request.GET["correo"] and request.GET["codigo"] and request.GET["password"]:
        nombre=request.GET["nombre"]
        apellidos=request.GET["apellidos"]
        correo = request.GET["correo"]
        code = request.GET["codigo"]
        tipoUsuario = 1
        passUser = request.GET["password"]
        u = Usuarios.objects.filter(codigo=code, tipo_usuario=1)
        u.exists()
        if u:
            userbbdd = Usuarios(code, correo, nombre, apellidos, passUser, tipoUsuario)
            userbbdd.save()
            user = User.objects.get(email=correo)
            user.set_username=correo
            user.set_password(passUser)
            user.save()
            return render(request, "endSuperUser.html")
        else:
            mensaje="El Código de administrador introducido no existe."
            return render(request,"altaEmptySuperUser.html",{"mensaje":mensaje})

    else:
        mensaje="Por favor, rellene todos los campos antes de modificar el Administrador."
        return render(request, "modEmptySuperUser.html",{"mensaje":mensaje})

def eliminarSuperUser(request):
    return render(request,"eliminarSuperUser.html")
def eliminarSuperUserData(request):
    if request.GET["codigo"]:
        mail=request.GET["codigo"]
        p = Usuarios.objects.filter(correo=mail, tipo_usuario=1)
        if p:
            request.session['mail'] = mail  # asi podemos pasar variables entre vistas
            u = Usuarios.objects.get(correo=mail)
            return render(request, "eliminarSuperUserConfirm.html",{"usuario":u})
        else:
            mensaje = "El correo de administrador introducido no existe."
            return render(request, "eliminarEmptySuperUsuarios.html", {"mensaje": mensaje})
    else:
        mensaje = "Por favor, rellene todos los campos antes de eliminar el administrador."
        return render(request, "eliminarEmptySuperUsuarios.html", {"mensaje": mensaje})
def eliminarSuperUserConfirm(request):
    eleccion = request.GET["choose"]
    if eleccion == "Eliminar":
        mail = request.session.get('mail')  # asi podemos recoger variables entre vistas
        User.objects.get(email=mail).delete()
        d = Usuarios.objects.get(correo=mail)
        d.delete()
        return render(request, "endUser.html")
    elif eleccion == "Cancelar":
        return render(request, "eliminarSuperUser.html")
## FILTADO DE DISPOSITIVOS
def filtrar(request):
    if request.user.is_authenticated:
        tipo = request.GET["tipo"]
        if tipo=="TODOS":
            dispositivo=Dispositivos.objects.all()
            depar = Departamentos.objects.all()
            return render(request, "dispositivos.html", {"dispositivo": dispositivo, "departamento": depar})
        else:
            dispositivo=Dispositivos.objects.filter(tipo=tipo)
            depar = Departamentos.objects.all()
            return render(request, "dispositivos.html", {"dispositivo": dispositivo, "departamento": depar})
    else:
        return render(request, "log.html")

def altadisp(request):
    return render(request,"alta.html")
def altadata(request):
    if request.GET["serial"] and request.GET["tipo"] and request.GET["marca"] and request.GET["modelo"] and request.GET["depar"]:
        serial=request.GET["serial"]
        tipo=request.GET["tipo"]
        marca = request.GET["marca"]
        modelo = request.GET["modelo"]
        depar = request.GET["depar"]
        p = Departamentos.objects.filter(id_departamento=depar)
        p.exists()
        if p:
            d=Dispositivos.objects.filter(serial_number=serial)
            d.exists()
            if d:
                mensaje = "El número de serie ya existe."
                return render(request, "altaempty.html", {"mensaje": mensaje})
            else:
                d = Dispositivos(serial, tipo, marca,modelo,depar)
                d.save()
            return render(request, "enddisp.html")
        else:
            mensaje="El departamento introducido no existe."
            return render(request, "altaempty.html",{"mensaje":mensaje})

    else:
        mensaje="Por favor, rellene todos los campos antes de registrar el dispositivo."
        return render(request, "altaempty.html",{"mensaje":mensaje})
def moddisp(request):
    return render(request,"modificarsearch.html")
def datasearch(request):
    if request.GET["serial"]:
        serial=request.GET["serial"]
        d = Dispositivos.objects.filter(serial_number=serial).first()
        d2 = Dispositivos.objects.filter(serial_number=serial).exists()
        if d2:
            tipo= d.tipo
            marca = d.marca
            modelo = d.modelo
            depar = d.id_departamento.id_departamento
            return render(request, "modificar.html", {"serial":serial,"tipo":tipo,"marca":marca,"modelo":modelo,"depar":depar})
        elif d2 == False:
            mensaje = "El serial number introducido no existe."
            return render(request, "modificarsearchempty.html", {"mensaje": mensaje})
    else:
        mensaje = "Por favor, rellene todos los campos antes de registrar el dispositivo."
        return render(request, "modificarsearchempty.html", {"mensaje": mensaje})
def moddata(request):
    if request.GET["serial"] and request.GET["tipo"] and request.GET["marca"] and request.GET["modelo"] and request.GET["depar"]:
        serial=request.GET["serial"]
        tipo=request.GET["tipo"]
        marca = request.GET["marca"]
        modelo = request.GET["modelo"]
        depar = request.GET["depar"]
        p = Dispositivos.objects.filter(serial_number=serial).exists()
        p2 = Departamentos.objects.filter(id_departamento=depar).exists()
        if p and p2:
            d = Dispositivos.objects.get(serial_number=serial)
            d.tipo=tipo
            d.marca=marca
            d.modelo=modelo
            d.id_departamento=Departamentos.objects.get(id_departamento=depar)
            d.save()
            return render(request, "enddisp.html")
        elif p == False:
            mensaje = "El serial number introducido no existe."
            return render(request, "modificarempty.html", {"mensaje": mensaje})
        elif p2 == False:
            mensaje = "El departamento introducido no existe."
            return render(request, "modificarempty.html", {"mensaje": mensaje})
    else:
        mensaje = "Por favor, rellene todos los campos antes de registrar el dispositivo."
        return render(request, "modificarempty.html", {"mensaje": mensaje})
def bajadisp(request):
    return render(request,"eliminar.html")
def eliminardata(request):
    if request.GET["serial"]:
        serial=request.GET["serial"]
        p = Dispositivos.objects.filter(serial_number=serial)
        if p:
            request.session['serial'] = serial  # asi podemos pasar variables entre vistas
            dispositivo = Dispositivos.objects.get(serial_number=serial)
            return render(request, "eliminarconfirm.html", {"dispositivo": dispositivo})
        else:
            mensaje = "El serial number introducido no existe."
            return render(request, "eliminarempty.html", {"mensaje": mensaje})
    else:
        mensaje = "Por favor, rellene todos los campos antes de registrar el dispositivo."
        return render(request, "eliminarempty.html", {"mensaje": mensaje})

def bajadispconfirm(request):
    eleccion = request.GET["choose"]
    if eleccion == "Eliminar":
        serial = request.session.get('serial')  # asi podemos recoger variables entre vistas
        d = Dispositivos.objects.filter(serial_number=serial)
        d.delete()
        return render(request,"enddisp.html")
    elif eleccion == "Cancelar":
        return render(request,"eliminar.html")
# ACTUALIZAR DATOS DE LA LISTA DE INCIDENCIAS
def ActualizarIncidencias(request):
    if request.GET["alta"] and request.GET["seleccion"] and request.GET["codigo"] and request.GET["serial"] and request.GET["tipo"] and request.GET["prioridad"]:
        codigo = request.session.get('codigo')
        state=request.GET["seleccion"]
        num_alta=request.GET["alta"]
        estado =request.GET['tipo']
        print(state)
        operador = request.GET['codigo']
        ope = Usuarios.objects.filter(codigo=operador).first()
        emailOperador = ope.correo
        print(emailOperador)
        startdate = datetime.now().date()
        if state == "3":
            SolucionIncidencia.objects.create(fecha_fin=startdate,tecnico=codigo,numero_alta=AltaIncidencia.objects.get(numero_alta=num_alta))
            print("Solucion realizada")
            asunto = 'Su incidencia ha sido finalizada.'
            email_from = settings.EMAIL_HOST_USER
            email_to = [emailOperador]
            email_mensaje = "Se le informa que la incidencia con numero de alta %s ha sido finalizada\nPuede valorarla desde " \
                            "(adjuntar enlace) o en la sección 'Consultar' de la App de Soan Technologies." % (num_alta)
            send_mail(asunto, email_mensaje, email_from, email_to, fail_silently=False)

        print("Solucion NO realizada")
        # recogemos el numero de error del string tipo de error
        error=Errores.objects.filter(tipo_error=estado).first()
        id=error.iderror
        #print(int(id))
        alta=AltaIncidencia(numero_alta=num_alta,fecha_inicio=request.GET["fechaInicio"],estado=request.GET["seleccion"],codigo=Usuarios.objects.get(codigo=request.GET["codigo"]),iderror=Errores.objects.get(iderror=id),serial_number=Dispositivos.objects.get(serial_number=request.GET["serial"]))
        alta.save()
        guardado=num_alta
        request.session['guardado']=guardado #asi podemos pasar variables entre vistas

        #COMPROBAMOS EL VALOR QUE SACA POR CONSOLA
        #print(guardado)

    return redirect(request.META['HTTP_REFERER'])

# Esta es la la vista que funciona para django, para que no
def ListadoIncidencias(request):
    if request.user.is_authenticated:
        guardado=request.session.get('guardado') #asi podemos recoger variables entre vistas
        incidencia=AltaIncidencia.objects.all().order_by('iderror__prioridad')
        incidencia2=AltaIncidencia.objects.all().values()
        estado2="En proceso"
        estado1="Iniciada"
        codigo = request.session.get('codigo')

        return render(request, "ListadoIncidencias.html",{"incidencia": incidencia,"incidencia2":incidencia2,"guardado":guardado,"estado1":estado1,"estado2":estado2,"codigo":codigo})
    else:
        return render(request, "log.html")

def ListadoResueltas(request):
    if request.user.is_authenticated:
        incidencia=SolucionIncidencia.objects.all().order_by('-numero_solucion')
        incidencia2 = AltaIncidencia.objects.all()
        return render(request, "ListadoResueltas.html",{"incidencia": incidencia,"incidencia2": incidencia2})
    else:
        return render(request, "log.html")

## VISTA DEL FORMULARIO DEL CLIENTE
def formulario(request):
    return render(request,"formulario.html")

def envioFormulario(request):
    if request.GET['num_incidencia']:
        incidencia=request.GET['num_incidencia']
        valoracion=request.GET['valoracion']
        s=SolucionIncidencia.objects.filter(numero_alta=incidencia).exists()
        if s:
            if SolucionIncidencia.objects.filter(numero_alta=incidencia, valoracion = None):
                d = SolucionIncidencia.objects.get(numero_alta=incidencia)
                d.valoracion = valoracion
                d.fecha_fin = d.fecha_fin
                d.tecnico = d.tecnico
                d.numero_alta = d.numero_alta
                d.save()
            else:
                mensaje = "La incidencia introducida ya ha sido valorada."
                return render(request, "formularioerror.html", {"mensaje": mensaje})
        else:
            mensaje="El numero de alta introducido no existe o no se ha solucionado aún."
            return render(request,"formularioerror.html",{"mensaje":mensaje})
        return render(request,"inicio.html")
    else:
        mensaje = "Rellena los campos antes de realizar la valoración."
        print("x")
        return render(request, "formularioerror.html", {"mensaje": mensaje})




