#!/usr/bin/python3.10

import sys
import os

# Agregar el directorio del proyecto al path
project_home = '/home/tuusuario/Incorporacion'  # Cambiar 'tuusuario' por tu usuario
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Importar la aplicación
from app import app as application

if __name__ == "__main__":
    application.run()