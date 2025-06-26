import os
import time
from datetime import datetime
from flask import render_template, request, jsonify
from config.config import IMAGES_FOLDER, PDFS_FOLDER
from app import app
from views import * 
from config.config import obtener_conexion


@app.route('/modal_add_aspirante', methods=['GET'])
def modal_add_aspirante():
    return render_template('aspirantes/modales/modalAdd.html')

@app.route('/add_aspirante', methods=['POST'])
def add_aspirante():
    try:
        # Pequeña pausa para asegurar que los archivos se guarden completamente
        time.sleep(0.5)
        
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        sexo = request.form.get('sexo')
        curso = request.form.get('curso')
        habla_ingles = request.form.get('habla_ingles')
        # Convertir el valor de habla_ingles a booleano
        habla_ingles = 1 if habla_ingles == 'on' else 0
        
        # Manejo de archivos
        imagen_perfil = request.files.get('imagen_perfil')
        archivo_pdf = request.files.get('archivo_pdf')
        
        # Generar nombres únicos para los archivos
        imagen_nombre = f"{nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        pdf_nombre = f"{nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Guardar archivos
        if imagen_perfil:
            imagen_perfil.save(os.path.join(IMAGES_FOLDER, imagen_nombre))
        if archivo_pdf:
            archivo_pdf.save(os.path.join(PDFS_FOLDER, pdf_nombre))
        
        # Almacenar solo las rutas en la base de datos
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO tbl_aspirantes (nombre, email, sexo, curso, habla_ingles, imagen_perfil, archivo_pdf) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                         (nombre, email, sexo, curso, habla_ingles, 
                          os.path.join('images', imagen_nombre) if imagen_perfil else None,
                          os.path.join('pdfs', pdf_nombre) if archivo_pdf else None))
            conexion.commit()
        return '', 200
    except Exception as e:
        print(f"Error al agregar aspirante: {e}")
        return jsonify({'error': str(e)}), 500 
    finally:
        conexion.close()      


@app.route('/modal_view_aspirante/<int:id>')
def ver_aspirante(id):
    aspirante = get_aspirante(id)
    return render_template('aspirantes/modales/modalView.html', aspirante=aspirante)

@app.route('/modal_update_aspirante/<int:id>')
def modal_update_aspirante(id):
    aspirante = get_aspirante(id)
    if aspirante:
        return render_template('aspirantes/modales/modalUpdate.html', aspirante=aspirante)
    return jsonify({'error': 'Aspirante no encontrado'}), 404


@app.route('/actualizar_aspirante/<int:id>', methods=['POST'])
def actualizar_aspirante(id):
    try:
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        sexo = request.form.get('sexo')
        curso = request.form.get('curso')
        habla_ingles = request.form.get('habla_ingles')
        habla_ingles = 1 if habla_ingles == 'on' else 0
        
        # Manejo de archivos
        imagen_perfil = request.files.get('imagen_perfil')
        archivo_pdf = request.files.get('archivo_pdf')
        
        # Generar nombres únicos para los archivos
        imagen_nombre = f"{nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg" if imagen_perfil else None
        pdf_nombre = f"{nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf" if archivo_pdf else None
        
        # Guardar archivos si existen
        if imagen_perfil:
            imagen_perfil.save(os.path.join(IMAGES_FOLDER, imagen_nombre))
        if archivo_pdf:
            archivo_pdf.save(os.path.join(PDFS_FOLDER, pdf_nombre))
        
        # Actualizar en la base de datos
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE tbl_aspirantes 
                SET nombre=%s, email=%s, sexo=%s, curso=%s, habla_ingles=%s,
                    imagen_perfil=%s, archivo_pdf=%s 
                WHERE id=%s
            """, 
            (nombre, email, sexo, curso, habla_ingles,
             os.path.join('images', imagen_nombre) if imagen_perfil else None,
             os.path.join('pdfs', pdf_nombre) if archivo_pdf else None,
             id))
            conexion.commit()
        return '', 200
    except Exception as e:
        print(f"Error al actualizar aspirante: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conexion' in locals():
            conexion.close()

@app.route('/modal_delete_aspirante/<int:id>')
def modal_delete_aspirante(id):
    aspirante = get_aspirante(id)
    if aspirante:
        return render_template('aspirantes/modales/modalDelete.html', aspirante=aspirante)
    return jsonify({'error': 'Aspirante no encontrado'}), 404


@app.route('/eliminar_aspirante/<int:id>', methods=['POST'])
def eliminar_aspirante(id):
    print('Llegando a eliminar aspirante con ID:', id)
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM tbl_aspirantes WHERE id = %s", (id,))
            conexion.commit()
        return '', 200
    except Exception as e:
        print(f"Error al eliminar aspirante: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conexion' in locals():
            conexion.close()

@app.route('/cambiar_estado/<int:id>', methods=['POST'])
def cambiar_estado_aspirante(id):
    cambiar_estado(id)
    return '', 200

# Ruta para la página de inicio
@app.route('/')
def home():
    aspirantes = get_aspirantes()
    return render_template('aspirantes/index.html', aspirantes=aspirantes)

# Lista de aspirantes
def get_aspirantes():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tbl_aspirantes ORDER BY id ASC")
            aspirantes = cursor.fetchall()
        return aspirantes 
    except Exception as e:
        print(f"Error obteniendo aspirantes: {e}")
        return "Error al obtener los aspirantes", 500
    finally:
        conexion.close()

def get_aspirante(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tbl_aspirantes WHERE id = %s", (id,))
            aspirante = cursor.fetchone()
        return aspirante
    except Exception as e:
        print(f"Error obteniendo aspirante: {e}")
        return "Error al obtener el aspirante", 500
    finally:
        conexion.close()


def cambiar_estado(id):
    try:
        aceptado = request.form.get('aceptado') == '1'
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE tbl_aspirantes SET aceptado = %s WHERE id = %s", (aceptado, id))
            conexion.commit()
        return ''
    except Exception as e:
        print(f"Error al cambiar estado: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conexion.close()