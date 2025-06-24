from flask import render_template, url_for
from app import app
from views import *

# Ruta para la página de inicio
@app.route('/')
def home():
    aspirantes = get_aspirantes()
    return render_template('aspirantes/index.html', aspirantes=aspirantes)

@app.route('/modal_add_aspirante', methods=['GET'])
def modal_add_aspirante():
    return render_template('aspirantes/modales/modalAdd.html')

@app.route('/modal_update_aspirante')
def modal_update_aspirante():
    return render_template('aspirantes/modales/modalUpdate.html')

@app.route('/modal_view_aspirante')
def modal_view_aspirante():
    return render_template('aspirantes/modales/modalView.html')

@app.route('/modal_view_aspirante/<int:id>')
def ver_aspirante(id):
    aspirante = get_aspirante(id)
    return render_template('aspirantes/modales/modalView.html', aspirante=aspirante)

@app.route('/modal_update_aspirante/<int:id>')
def editar_aspirante(id):
    aspirante = get_aspirante(id)
    return render_template('aspirantes/modales/modalUpdate.html', aspirante=aspirante)

@app.route('/modal_delete_aspirante/<int:id>')
def eliminar_aspirante(id):
    aspirante = get_aspirante(id)
    return render_template('aspirantes/modales/modalDelete.html', aspirante=aspirante)


@app.route('/cambiar_estado/<int:id>', methods=['POST'])
def cambiar_estado_aspirante(id):
    cambiar_estado(id)
    return '', 200