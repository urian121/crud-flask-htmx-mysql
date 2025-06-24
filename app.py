from flask import Flask

# Crear la app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['UPLOAD_FOLDER'] = 'static/uploads'


# Importar rutas después de crear la app
from urls import *


if __name__ == '__main__':
    app.run(debug=True, port=5000)