from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
import os
import json
import pandas as pd
from datetime import datetime
import io
from functools import wraps

app = Flask(__name__)

# Configuración básica
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui_muy_segura_2025'

# Usuarios del sistema
USUARIOS = {
    'admin': {
        'password': 'admin123',
        'rol': 'administrador',
        'nombre': 'Administrador del Sistema'
    },
    'usuario': {
        'password': 'user123',
        'rol': 'usuario',
        'nombre': 'Usuario Regular'
    }
}

# Archivo para almacenar las solicitudes (simulando una base de datos)
SOLICITUDES_FILE = 'solicitudes.json'

def cargar_solicitudes():
    """Cargar solicitudes desde el archivo JSON"""
    if os.path.exists(SOLICITUDES_FILE):
        try:
            with open(SOLICITUDES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def guardar_solicitudes(solicitudes):
    """Guardar solicitudes en el archivo JSON"""
    try:
        with open(SOLICITUDES_FILE, 'w', encoding='utf-8') as f:
            json.dump(solicitudes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error al guardar solicitudes: {e}")
        return False

def obtener_siguiente_id():
    """Obtener el siguiente ID disponible"""
    solicitudes = cargar_solicitudes()
    if not solicitudes:
        return 1
    return max(s.get('id', 0) for s in solicitudes) + 1

def login_required(f):
    """Decorador para requerir login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return jsonify({'error': 'No autorizado', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para requerir permisos de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return jsonify({'error': 'No autorizado', 'redirect': '/login'}), 401
        if session.get('rol') != 'administrador':
            return jsonify({'error': 'Permisos insuficientes'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Ruta principal que renderiza el template de incorporación"""
    return render_template('incorporacion.html')

@app.route('/incorporacion')
def incorporacion():
    """Ruta específica para el proceso de incorporación"""
    return render_template('incorporacion.html')

@app.route('/api/login', methods=['POST'])
def login():
    """API endpoint para autenticación de usuarios"""
    try:
        data = request.get_json()
        usuario = data.get('usuario')
        password = data.get('password')
        
        if not usuario or not password:
            return jsonify({
                'success': False,
                'error': 'Usuario y contraseña son requeridos'
            }), 400
        
        # Verificar credenciales
        if usuario in USUARIOS and USUARIOS[usuario]['password'] == password:
            # Crear sesión
            session['usuario'] = usuario
            session['rol'] = USUARIOS[usuario]['rol']
            session['nombre'] = USUARIOS[usuario]['nombre']
            
            return jsonify({
                'success': True,
                'usuario': usuario,
                'rol': USUARIOS[usuario]['rol'],
                'nombre': USUARIOS[usuario]['nombre'],
                'message': 'Login exitoso'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Credenciales inválidas'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """API endpoint para cerrar sesión"""
    try:
        session.clear()
        return jsonify({
            'success': True,
            'message': 'Sesión cerrada correctamente'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session', methods=['GET'])
def get_session():
    """API endpoint para obtener información de la sesión actual"""
    try:
        if 'usuario' in session:
            return jsonify({
                'authenticated': True,
                'usuario': session['usuario'],
                'rol': session['rol'],
                'nombre': session['nombre']
            })
        else:
            return jsonify({
                'authenticated': False
            })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/solicitudes', methods=['GET'])
def obtener_solicitudes():
    """API endpoint para obtener todas las solicitudes"""
    try:
        solicitudes = cargar_solicitudes()
        return jsonify(solicitudes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/solicitudes', methods=['POST'])
def crear_solicitud():
    """API endpoint para crear una nueva solicitud"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        campos_requeridos = [
            'nombres_completos', 'dni', 'profesion', 'empresa', 
            'cargo', 'sector', 'fecha_nacimiento'
        ]
        
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({
                    'success': False, 
                    'error': f'El campo {campo} es requerido'
                }), 400
        
        # Cargar solicitudes existentes
        solicitudes = cargar_solicitudes()
        
        # Verificar si ya existe una solicitud con el mismo DNI
        dni_existente = any(s.get('dni') == data.get('dni') for s in solicitudes)
        if dni_existente:
            return jsonify({
                'success': False,
                'error': 'Ya existe una solicitud con este DNI'
            }), 400
        
        # Crear nueva solicitud
        nueva_solicitud = {
            'id': obtener_siguiente_id(),
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'nombres_completos': data.get('nombres_completos'),
            'dni': data.get('dni'),
            'profesion': data.get('profesion'),
            'empresa': data.get('empresa'),
            'cargo': data.get('cargo'),
            'sector': data.get('sector'),
            'fecha_nacimiento': data.get('fecha_nacimiento'),
            'estado': 'Pendiente',
            'evaluador': '',
            'observaciones': ''
        }
        
        # Agregar a la lista y guardar
        solicitudes.append(nueva_solicitud)
        
        if guardar_solicitudes(solicitudes):
            return jsonify({
                'success': True,
                'id': nueva_solicitud['id'],
                'message': 'Solicitud creada correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al guardar la solicitud'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/solicitudes/<int:solicitud_id>', methods=['PATCH'])
def actualizar_solicitud(solicitud_id):
    """API endpoint para actualizar una solicitud (evaluación)"""
    try:
        data = request.get_json()
        solicitudes = cargar_solicitudes()
        
        # Buscar la solicitud
        solicitud_encontrada = None
        for i, solicitud in enumerate(solicitudes):
            if solicitud.get('id') == solicitud_id:
                solicitud_encontrada = i
                break
        
        if solicitud_encontrada is None:
            return jsonify({
                'success': False,
                'error': 'Solicitud no encontrada'
            }), 404
        
        # Actualizar campos permitidos
        campos_actualizables = ['estado', 'evaluador', 'observaciones']
        for campo in campos_actualizables:
            if campo in data:
                solicitudes[solicitud_encontrada][campo] = data[campo]
        
        # Agregar fecha de evaluación
        solicitudes[solicitud_encontrada]['fecha_evaluacion'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        if guardar_solicitudes(solicitudes):
            return jsonify({
                'success': True,
                'message': 'Solicitud actualizada correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al actualizar la solicitud'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/solicitudes/<int:solicitud_id>', methods=['GET'])
def obtener_solicitud(solicitud_id):
    """API endpoint para obtener una solicitud específica"""
    try:
        solicitudes = cargar_solicitudes()
        
        for solicitud in solicitudes:
            if solicitud.get('id') == solicitud_id:
                return jsonify(solicitud)
        
        return jsonify({
            'error': 'Solicitud no encontrada'
        }), 404
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/solicitudes/<int:solicitud_id>', methods=['DELETE'])
def eliminar_solicitud(solicitud_id):
    """API endpoint para eliminar una solicitud"""
    try:
        solicitudes = cargar_solicitudes()
        
        # Filtrar la solicitud a eliminar
        solicitudes_filtradas = [s for s in solicitudes if s.get('id') != solicitud_id]
        
        if len(solicitudes_filtradas) == len(solicitudes):
            return jsonify({
                'success': False,
                'error': 'Solicitud no encontrada'
            }), 404
        
        if guardar_solicitudes(solicitudes_filtradas):
            return jsonify({
                'success': True,
                'message': 'Solicitud eliminada correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al eliminar la solicitud'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/descargar_solicitudes_excel')
def descargar_excel():
    """Endpoint para descargar las solicitudes en formato Excel"""
    try:
        solicitudes = cargar_solicitudes()
        
        if not solicitudes:
            return jsonify({
                'error': 'No hay solicitudes para descargar'
            }), 404
        
        # Crear DataFrame
        df = pd.DataFrame(solicitudes)
        
        # Reordenar columnas para mejor presentación (sin evaluador y observaciones)
        columnas_orden = [
            'id', 'fecha', 'nombres_completos', 'dni', 'profesion', 
            'empresa', 'cargo', 'sector', 'fecha_nacimiento', 'estado'
        ]
        
        # Filtrar solo las columnas que existen
        columnas_existentes = [col for col in columnas_orden if col in df.columns]
        df = df[columnas_existentes]
        
        # Renombrar columnas para mejor legibilidad
        nombres_columnas = {
            'id': 'ID',
            'fecha': 'Fecha Solicitud',
            'nombres_completos': 'Nombres Completos',
            'dni': 'DNI',
            'profesion': 'Profesión',
            'empresa': 'Empresa',
            'cargo': 'Cargo',
            'sector': 'Sector',
            'fecha_nacimiento': 'Fecha Nacimiento',
            'estado': 'Estado'
        }
        
        df = df.rename(columns=nombres_columnas)
        
        # Crear archivo Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Solicitudes', index=False)
            
            # Obtener el workbook y worksheet para formatear
            workbook = writer.book
            worksheet = writer.sheets['Solicitudes']
            
            # Importar estilos de openpyxl para formateo
            from openpyxl.styles import Alignment, Font, PatternFill
            
            # Formatear encabezados
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Centrar la columna ID (columna A)
            for row in range(2, worksheet.max_row + 1):
                cell = worksheet[f'A{row}']
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Ajustar ancho de columnas
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        
        # Generar nombre de archivo con fecha
        fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f'solicitudes_incorporacion_{fecha_actual}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=nombre_archivo
        )
        
    except Exception as e:
        return jsonify({
            'error': f'Error al generar Excel: {str(e)}'
        }), 500

@app.route('/api/estadisticas')
def obtener_estadisticas():
    """API endpoint para obtener estadísticas de las solicitudes"""
    try:
        solicitudes = cargar_solicitudes()
        
        total = len(solicitudes)
        pendientes = len([s for s in solicitudes if s.get('estado') == 'Pendiente'])
        aprobadas = len([s for s in solicitudes if s.get('estado') == 'Aprobado'])
        rechazadas = len([s for s in solicitudes if s.get('estado') == 'Rechazado'])
        
        # Estadísticas por sector
        sectores = {}
        for solicitud in solicitudes:
            sector = solicitud.get('sector', 'No especificado')
            sectores[sector] = sectores.get(sector, 0) + 1
        
        # Estadísticas por mes
        solicitudes_por_mes = {}
        for solicitud in solicitudes:
            try:
                fecha = datetime.strptime(solicitud.get('fecha', ''), '%Y-%m-%d %H:%M')
                mes_año = fecha.strftime('%Y-%m')
                solicitudes_por_mes[mes_año] = solicitudes_por_mes.get(mes_año, 0) + 1
            except:
                pass
        
        return jsonify({
            'total': total,
            'pendientes': pendientes,
            'aprobadas': aprobadas,
            'rechazadas': rechazadas,
            'por_sector': sectores,
            'por_mes': solicitudes_por_mes
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/status')
def api_status():
    """API endpoint para verificar el estado del servidor"""
    return jsonify({
        'status': 'active',
        'message': 'Servidor de incorporación funcionando correctamente',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Manejador de errores 404"""
    return jsonify({
        'error': 'Endpoint no encontrado',
        'status': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejador de errores 500"""
    return jsonify({
        'error': 'Error interno del servidor',
        'status': 500
    }), 500

# Inicialización para Vercel
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/images', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Crear archivo de solicitudes si no existe
if not os.path.exists(SOLICITUDES_FILE):
    guardar_solicitudes([])

if __name__ == '__main__':
    print("🚀 Iniciando servidor de incorporación...")
    print("📋 Sistema de gestión para nuevos asociados")
    print("🌐 Accede a: http://localhost:5000")
    print("📊 API disponible en: http://localhost:5000/api/")
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)