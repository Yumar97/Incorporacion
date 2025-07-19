# 🏢 Sistema de Incorporación - YmPeru

Sistema web profesional para la gestión de solicitudes de incorporación de nuevos asociados con proceso de evaluación automatizado.

## ✨ Características

- 🔐 **Sistema de autenticación** con dos tipos de usuarios
- 👥 **Gestión de solicitudes** completa
- 📊 **Descarga de reportes** en Excel
- 🎨 **Interfaz moderna** con React y Tailwind CSS
- 📱 **Diseño responsive** para todos los dispositivos

## 👤 Usuarios del Sistema

### Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Aprobar/rechazar solicitudes, ver detalles completos

### Usuario Regular
- **Usuario:** `usuario`
- **Contraseña:** `user123`
- **Permisos:** Enviar solicitudes, ver estado

## 🚀 Tecnologías

- **Backend:** Flask (Python)
- **Frontend:** React + Tailwind CSS
- **Base de datos:** JSON (archivo local)
- **Reportes:** Pandas + OpenPyXL

## 📦 Instalación Local

1. Clona el repositorio:
```bash
git clone <tu-repositorio>
cd VersionFinal_Incorporacion
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
python app.py
```

4. Abre tu navegador en: `http://localhost:5000`

## 🌐 Deploy en Vercel

Este proyecto está configurado para deployarse automáticamente en Vercel.

## 📋 Estructura del Proyecto

```
VersionFinal_Incorporacion/
├── templates/
│   └── incorporacion.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── images/
├── app.py
├── requirements.txt
├── vercel.json
└── README.md
```

## 👨‍💻 Desarrollado por

**Yumar Manrique Araujo** - Ingeniero de Sistemas
- 📱 943039019
- ✉️ yumar.manrique@gmail.com

---

© 2025 YmPeru. Todos los derechos reservados.