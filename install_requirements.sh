#!/bin/bash

# Script para instalar requerimientos en PythonAnywhere
# Ejecutar con: bash install_requirements.sh

echo "🚀 Iniciando instalación de dependencias para PythonAnywhere..."
echo "=================================================="

# Verificar la versión de Python
echo "📋 Verificando versión de Python..."
python3.10 --version

# Actualizar pip
echo "🔄 Actualizando pip..."
python3.10 -m pip install --user --upgrade pip

# Instalar dependencias desde requirements.txt
echo "📦 Instalando dependencias desde requirements.txt..."
pip3.10 install --user -r requirements.txt

# Verificar instalaciones
echo "✅ Verificando instalaciones..."
echo "=================================================="

echo "Flask:"
python3.10 -c "import flask; print(f'✓ Flask {flask.__version__}')" 2>/dev/null || echo "✗ Flask no instalado"

echo "Flask-SQLAlchemy:"
python3.10 -c "import flask_sqlalchemy; print(f'✓ Flask-SQLAlchemy {flask_sqlalchemy.__version__}')" 2>/dev/null || echo "✗ Flask-SQLAlchemy no instalado"

echo "Pandas:"
python3.10 -c "import pandas; print(f'✓ Pandas {pandas.__version__}')" 2>/dev/null || echo "✗ Pandas no instalado"

echo "OpenPyXL:"
python3.10 -c "import openpyxl; print(f'✓ OpenPyXL {openpyxl.__version__}')" 2>/dev/null || echo "✗ OpenPyXL no instalado"

echo "Werkzeug:"
python3.10 -c "import werkzeug; print(f'✓ Werkzeug {werkzeug.__version__}')" 2>/dev/null || echo "✗ Werkzeug no instalado"

# Verificar estructura de archivos
echo ""
echo "📁 Verificando estructura de archivos..."
echo "=================================================="

files=("app.py" "wsgi.py" "config.py" "requirements.txt" "templates/incorporacion.html" "static/css/styles.css")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (faltante)"
    fi
done

# Verificar permisos
echo ""
echo "🔐 Verificando permisos..."
echo "=================================================="
ls -la app.py wsgi.py config.py 2>/dev/null || echo "Algunos archivos no encontrados"

# Crear base de datos si no existe
echo ""
echo "🗄️ Inicializando base de datos..."
echo "=================================================="
python3.10 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de datos inicializada correctamente')
" 2>/dev/null || echo "⚠️ Error al inicializar base de datos (normal si hay problemas de importación)"

# Mostrar resumen
echo ""
echo "📊 RESUMEN DE INSTALACIÓN"
echo "=================================================="
echo "Directorio actual: $(pwd)"
echo "Usuario: $(whoami)"
echo "Fecha: $(date)"

# Mostrar paquetes instalados
echo ""
echo "📦 Paquetes Python instalados (relacionados con Flask):"
pip3.10 list --user | grep -i flask
pip3.10 list --user | grep -i pandas
pip3.10 list --user | grep -i openpyxl
pip3.10 list --user | grep -i werkzeug

echo ""
echo "🎉 Instalación completada!"
echo "=================================================="
echo "Próximos pasos:"
echo "1. Ve al panel Web de PythonAnywhere"
echo "2. Configura el archivo WSGI con la ruta correcta"
echo "3. Recarga tu aplicación web"
echo "4. Revisa los logs si hay errores"
echo ""
echo "Para más ayuda, consulta: README_PYTHONANYWHERE.md"