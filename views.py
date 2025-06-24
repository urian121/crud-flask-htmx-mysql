from config.config import obtener_conexion

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