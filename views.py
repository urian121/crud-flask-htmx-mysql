import os
import time
from datetime import datetime
from flask import render_template, request, jsonify
from config.config import IMAGES_FOLDER, PDFS_FOLDER
from views import * 
from config.config import obtener_conexion

# Ruta de la página principal
def home():
    aspirantes = get_aspirantes()
    return render_template('aspirantes/index.html', aspirantes=aspirantes)

# Modal para agregar un aspirante
def modal_add_aspirante():
    return render_template('aspirantes/modales/modalAdd.html')

# Agregar un aspirante
def add_aspirante():
    try:
        time.sleep(0.5) # Pequeña pausa de 0.5 segundos
        
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

        ruta_imagen = procesar_archivo(imagen_perfil)
        ruta_pdf = procesar_archivo(archivo_pdf)        
        
        # Almacenar solo las rutas en la base de datos
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO tbl_aspirantes (nombre, email, sexo, curso, habla_ingles, imagen_perfil, archivo_pdf) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                         (nombre, email, sexo, curso, habla_ingles, ruta_imagen, ruta_pdf))
            conexion.commit()

            # Obtener el ID del nuevo aspirante
            nuevo_id = cursor.lastrowid
            
            # Devolver la fila HTML del nuevo aspirante
            return get_fila_aspirante(nuevo_id)
    except Exception as e:
        print(f"Error al agregar aspirante: {e}")
        return jsonify({'error': str(e)}), 500 
    finally:
        conexion.close()      

# Modal para ver un aspirante
def ver_aspirante(id):
    aspirante = get_aspirante(id)
    return render_template('aspirantes/modales/modalView.html', aspirante=aspirante)

# Modal para actualizar un aspirante
def modal_update_aspirante(id):
    aspirante = get_aspirante(id)
    if aspirante:
        return render_template('aspirantes/modales/modalUpdate.html', aspirante=aspirante)
    return jsonify({'error': 'Aspirante no encontrado'}), 404

# Actualizar un aspirante
def actualizar_aspirante(id):
    try:
        time.sleep(0.5) # Pequeña pausa de 0.5 segundos
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        sexo = request.form.get('sexo')
        curso = request.form.get('curso')
        habla_ingles = request.form.get('habla_ingles')
        habla_ingles = 1 if habla_ingles == 'on' else 0
        
        # Manejo de archivos
        imagen_perfil = request.files.get('imagen_perfil')
        archivo_pdf = request.files.get('archivo_pdf')
        
        # Actualizar en la base de datos
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Base del update
            sql = """
                UPDATE tbl_aspirantes SET
                nombre=%s, email=%s, sexo=%s, curso=%s, habla_ingles=%s
            """
            valores = [nombre, email, sexo, curso, habla_ingles]

            # Si existe el archivo imagen_perfil y además tiene nombre (es decir, no está vacío)
            if imagen_perfil and imagen_perfil.filename:
                ruta_imagen = procesar_archivo(imagen_perfil)
                sql += ", imagen_perfil=%s"
                valores.append(ruta_imagen)

            # Si existe el archivo archivo_pdf y además tiene nombre (es decir, no está vacío)
            if archivo_pdf and archivo_pdf.filename:
                ruta_pdf = procesar_archivo(archivo_pdf)
                sql += ", archivo_pdf=%s"
                valores.append(ruta_pdf)

            sql += " WHERE id=%s"
            valores.append(id)

            cursor.execute(sql, valores)
            conexion.commit()

            # Devolver la fila HTML actualizada
            return get_fila_aspirante(id)
    except Exception as e:
        print(f"Error al actualizar aspirante: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conexion' in locals():
            conexion.close()

# Modal para eliminar un aspirante
def modal_delete_aspirante(id):
    aspirante = get_aspirante(id)
    if aspirante:
        return render_template('aspirantes/modales/modalDelete.html', aspirante=aspirante)
    return jsonify({'error': 'Aspirante no encontrado'}), 404

# Eliminar un aspirante
def eliminar_aspirante(id):
    try:
        # Pequeña pausa para asegurar que los archivos se guarden completamente
        time.sleep(0.5) # Pequeña pausa de 0.5 segundos
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM tbl_aspirantes WHERE id = %s", (id,))
            conexion.commit()
        return '', 204 # Devolver 204 No Content para indicar éxito
    except Exception as e:
        print(f"Error al eliminar aspirante: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conexion' in locals():
            conexion.close()

# Cambiar el estado de un aspirante
def cambiar_estado_aspirante(id):
    try:
        aceptado = request.form.get('aceptado') == '1'
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE tbl_aspirantes SET aceptado = %s WHERE id = %s", (aceptado, id))
            conexion.commit()
        return '', 200
    except Exception as e:
        print(f"Error al cambiar estado: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conexion.close()

# Obtener todos los aspirantes
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

# Obtener un aspirante por ID
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

# Función para procesar archivos
def procesar_archivo(archivo):
    if archivo:
        extension = archivo.filename.rsplit('.', 1)[-1].lower()
        carpeta = PDFS_FOLDER if extension == 'pdf' else IMAGES_FOLDER

        nombre_archivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
        ruta_completa = os.path.join(carpeta, nombre_archivo)

        archivo.save(ruta_completa)

        return os.path.join(os.path.basename(carpeta), nombre_archivo)
    return None


# Obtiene la fila HTML para un aspirante específico
def get_fila_aspirante(id):
    aspirante = get_aspirante(id)
    return render_template('aspirantes/fila.html', aspirante=aspirante)
