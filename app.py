from flask import Flask
from flask import redirect, url_for
from router import register_routes

# Crear la app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Registrar todas las rutas
register_routes(app)

# Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=8500)