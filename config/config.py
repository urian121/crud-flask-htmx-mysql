import pymysql
from pymysql.cursors import DictCursor
import os

# Rutas para archivos
UPLOAD_FOLDER = os.path.join('static', 'uploads')
IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER, 'images')
PDFS_FOLDER = os.path.join(UPLOAD_FOLDER, 'pdfs')

# Verificar y crear las carpetas si no existen
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(PDFS_FOLDER, exist_ok=True)


# Conexión a la base de datos MySQL
def obtener_conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="4825",
        db="bd_crud_flask_htmx_mysql",
        cursorclass=DictCursor
    )