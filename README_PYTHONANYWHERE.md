# Configuración para PythonAnywhere

## Pasos para solucionar el error "Something went wrong"

### 1. Verificar la configuración del WSGI

Asegúrate de que el archivo `wsgi.py` tenga la ruta correcta:
```python
project_home = '/home/incorporacion/Incorporacion'
```

### 2. Instalar dependencias

En la consola de PythonAnywhere, ejecuta:
```bash
pip3.10 install --user -r requirements.txt
```

### 3. Configurar la aplicación web

En el panel de PythonAnywhere:
- Ve a "Web" → "incorporacion.pythonanywhere.com"
- En "Code", asegúrate de que:
  - Source code: `/home/incorporacion/Incorporacion`
  - Working directory: `/home/incorporacion/Incorporacion`
  - WSGI configuration file: `/var/www/incorporacion_pythonanywhere_com_wsgi.py`

### 4. Verificar el archivo WSGI en PythonAnywhere

El archivo WSGI en PythonAnywhere debe contener:
```python
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
```

### 5. Verificar los logs

Revisa los logs de error en:
- incorporacion.pythonanywhere.com.error.log
- incorporacion.pythonanywhere.com.server.log

### 6. Problemas comunes y soluciones

#### Error de importación
- Verifica que todas las dependencias estén instaladas
- Asegúrate de que el path del proyecto sea correcto

#### Error de base de datos
- La base de datos SQLite se creará automáticamente
- Verifica permisos de escritura en el directorio

#### Error de templates
- Asegúrate de que exista la carpeta `templates/`
- Verifica que `incorporacion.html` esté presente

### 7. Reiniciar la aplicación

Después de hacer cambios:
1. Ve al panel "Web"
2. Haz clic en "Reload incorporacion.pythonanywhere.com"

### 8. Variables de entorno (opcional)

Puedes configurar variables de entorno en el archivo WSGI:
```python
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'
```

### 9. Estructura de archivos esperada

```
/home/incorporacion/Incorporacion/
├── app.py
├── wsgi.py
├── config.py
├── requirements.txt
├── templates/
│   └── incorporacion.html
├── static/
│   └── css/
│       └── styles.css
└── solicitudes.db (se crea automáticamente)
```

### 10. Comandos útiles en la consola

```bash
# Verificar la versión de Python
python3.10 --version

# Verificar dependencias instaladas
pip3.10 list --user

# Verificar estructura de archivos
ls -la /home/incorporacion/Incorporacion/

# Probar la aplicación localmente
cd /home/incorporacion/Incorporacion/
python3.10 app.py
```