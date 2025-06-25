from flask import Flask
from flask import redirect, url_for

# Crear la app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['UPLOAD_FOLDER'] = 'static/uploads'


# Importar rutas después de crear la app
from urls import *


# Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8500)