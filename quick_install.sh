#!/bin/bash

# Instalación rápida para PythonAnywhere
echo "Instalando dependencias..."

# Actualizar pip
python3.10 -m pip install --user --upgrade pip

# Instalar dependencias
pip3.10 install --user Flask==2.3.3
pip3.10 install --user Flask-SQLAlchemy==3.0.5
pip3.10 install --user pandas==2.0.3
pip3.10 install --user openpyxl==3.1.2
pip3.10 install --user Werkzeug==2.3.7

echo "✅ Instalación completada!"
echo "Recarga tu aplicación web en PythonAnywhere"