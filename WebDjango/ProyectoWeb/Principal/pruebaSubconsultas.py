
#Importar models
from Principal.models import *

incidencia = AltaIncidencia.objects.all()
for i in incidencia:
    print(i)
