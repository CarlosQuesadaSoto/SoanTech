"""ProyectoWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from Principal.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login),
    path('logindata/',takelogindata),
    path('', inicio),
    path('informacion/',informacion),
    path('cuenta/',cuenta),
    path('cerrarsesion/',cuentaout),
    path('ListadoIncidencias/',ListadoIncidencias),
    path('estadisticas/',estadisticas),
    path('usuarios/',usuarios),
    path('filtrarUsuarios/',filtrarUsuarios),
    path('altaUser/',altaUser),
    path('altaSuperUser/',altaSuperUser),
    path('altaUserData/',altaUserData),
    path('altaSuperUserData/', altaSuperUserData),
    path('modUser/',modUser),
    path('modUserSearch/',modUserSearch),
    path('modSuperUser/',modSuperUser),
    path('modUserData/',modUserData),
    path('modSuperUserSearch/',modSuperUserSearch),
    path('modSuperUserData/', modSuperUserData),
    path('eliminarUser/',eliminarUser),
    path('bajausuconfirm/',bajauserconfirm),
    path('eliminarSuperUser/',eliminarSuperUser),
    path('eliminarUserData/',eliminarUserData),
    path('eliminarSuperUserData/',eliminarSuperUserData),
    path('bajasuperconfirm/',eliminarSuperUserConfirm),
    path('dispositivos/',dispositivos),
    path('alta/',altadisp),
    path('altadata/',altadata),
    path('mod/',moddisp),
    path('datasearch/',datasearch),
    path('moddata/',moddata),
    path('baja/',bajadisp),
    path('bajadispconfirm/',bajadispconfirm),
    path('eliminardata/',eliminardata),
    path('ActualizarIncidencias/',ActualizarIncidencias),
    path('ListadoResueltas/', ListadoResueltas),
    path('back/',dispositivos),
    path('backUser/',usuarios),
    path('filtrar/',filtrar),
    path('filtrarstats/',filtrarstats),
    path('formulario/',formulario),
    path('envioFormulario/',envioFormulario),
    url(r'^api/data/$', getdata, name='api-data'), #para llamar al url-endpoint='{% url "api-data" %}'> --del script--
    url(r'^api/chart/data/$', ChartsData.as_view()), #para llamar al var endpoint =() del html
    url(r'^api/data/$', getdata, name='api-data'),
    url(r'^api/chart/dataultimaSemana/$', UltimaSemana.as_view()),
    url(r'^api/data/$', getdata, name='api-data'),
    url(r'^api/chart/dataultimoAño/$', UltimoAno.as_view()),
    url(r'^api/data/$', getdata, name='api-data'),
    url(r'^api/chart/dataultimoMes/$', UltimoMes.as_view()),

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
