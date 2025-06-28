# CRUD de Aspirantes con Flask + HTMX + MySQL

Este proyecto es un CRUD completo de aspirantes usando Flask, HTMX para interactividad sin recarga, y MySQL como base de datos. A continuación te explico brevemente la función de cada archivo principal.

![image](https://raw.githubusercontent.com/urian121/imagenes-proyectos-github/refs/heads/master/crud-flask-htmx-mysql.gif)

## 📁 app.py

Archivo principal que:

- Crea la instancia de Flask.
- Define configuraciones generales (`SECRET_KEY`, `UPLOAD_FOLDER`).
- Registra todas las rutas mediante `register_routes(app)` desde `router.py`.
- Maneja errores 404 mostrando una plantilla personalizada.
- Inicia el servidor en modo desarrollo (`debug=True`, puerto `8500`).


## 📁 router.py

Encargado de registrar todas las rutas de la app, de forma centralizada y ordenada. Usa `add_url_rule()` para asociar URLs con funciones de `views.py`.

Rutas incluidas:
- Home
- Crear, ver, actualizar, eliminar y cambiar estado de aspirantes
- Rutas de modales usadas con HTMX (`modal_add_aspirante`, etc.)


## 📁 views.py

Contiene la lógica de cada vista o funcionalidad:

- `home`: muestra la lista de aspirantes.
- `modal_add_aspirante`, `modal_update_aspirante`, `modal_view_aspirante`, etc.: renderizan modales HTML para usar con HTMX.
- `add_aspirante`, `actualizar_aspirante`: reciben formularios, guardan archivos y actualizan datos en MySQL.
- `eliminar_aspirante`: borra un registro.
- `cambiar_estado_aspirante`: activa o desactiva un aspirante.
- Funciones auxiliares como `get_aspirante()` o `get_aspirantes()` para interactuar con la base de datos.


## 📁 config/config.py *(no incluido aquí)*

Debe contener:
- Credenciales de conexión a MySQL.
- Rutas como `IMAGES_FOLDER` y `PDFS_FOLDER`.
- Función `obtener_conexion()` para conectarse a la DB.


## 🙌 Cómo puedes apoyar 📢:

✨ **Comparte este proyecto** con otros desarrolladores para que puedan beneficiarse 📢.

☕ **Invítame un café o una cerveza 🍺**:
   - [Paypal](https://www.paypal.me/iamdeveloper86) (`iamdeveloper86@gmail.com`).