import pymysql
from pymysql.cursors import DictCursor

# Conexión a la base de datos MySQL
def obtener_conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="bd_crud_flask_htmx_mysql",
        cursorclass=DictCursor
    )