from views import *

# Registrar rutas
def register_routes(app):
    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/modal_add_aspirante', 'modal_add_aspirante', modal_add_aspirante, methods=['GET'])
    app.add_url_rule('/add_aspirante', 'add_aspirante', add_aspirante, methods=['POST'])
    app.add_url_rule('/modal_view_aspirante/<int:id>', 'ver_aspirante', ver_aspirante)
    app.add_url_rule('/modal_update_aspirante/<int:id>', 'modal_update_aspirante', modal_update_aspirante)
    app.add_url_rule('/actualizar_aspirante/<int:id>', 'actualizar_aspirante', actualizar_aspirante, methods=['POST'])
    app.add_url_rule('/modal_delete_aspirante/<int:id>', 'modal_delete_aspirante', modal_delete_aspirante)
    app.add_url_rule('/eliminar_aspirante/<int:id>', 'eliminar_aspirante', eliminar_aspirante, methods=['POST'])
    app.add_url_rule('/cambiar_estado_aspirante/<int:id>', 'cambiar_estado_aspirante', cambiar_estado_aspirante, methods=['POST'])