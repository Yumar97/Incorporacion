#!/usr/bin/python3.10

import sys
import os

# Agregar el directorio del proyecto al path
project_home = '/home/incorporacion/Incorporacion'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Cambiar al directorio del proyecto
os.chdir(project_home)

# Importar la aplicación
from app import app as application

if __name__ == "__main__":
    application.run()