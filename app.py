# app.py
# Archivo principal de la aplicación Flask.
# Define las rutas (URLs) y conecta la interfaz con la lógica CRUD (models.py).

from flask import Flask, render_template, request, redirect, url_for

from database import inicializar_bd
from models import (
    registrar_paciente,
    listar_pacientes,
    obtener_paciente,
    eliminar_paciente,
    actualizar_paciente,
)

app = Flask(__name__)

# Al arrancar la aplicación se crea la base de datos y la tabla si no existen.
# Como database.py usa CREATE TABLE IF NOT EXISTS, ejecutar varias veces
# NO duplica la tabla ni genera error.
inicializar_bd()


@app.route("/")
def index():
    """
    Ruta principal (GET /): muestra el formulario de registro
    y la tabla con todos los pacientes ya registrados.
    """
    pacientes = listar_pacientes()
    return render_template("index.html", pacientes=pacientes)


@app.route("/registrar", methods=["POST"])
def registrar():
    """
    Procesa el envío del formulario (POST) para registrar un nuevo paciente.
    """
    # Se recogen los datos enviados desde el formulario HTML.
    # .strip() elimina espacios en blanco sobrantes al inicio y final.
    nombre_mascota = request.form.get("nombre_mascota", "").strip()
    especie = request.form.get("especie", "").strip()
    edad_texto = request.form.get("edad", "").strip()
    nombre_propietario = request.form.get("nombre_propietario", "").strip()
    telefono_propietario = request.form.get("telefono_propietario", "").strip()

    # -------------------------------------------------------------------
    # SEGURIDAD 2 (Validación de entradas antes de insertar en la BD):
    #
    # a) Se verifica que los campos obligatorios no estén vacíos.
    # b) Se verifica que la edad sea un número ENTERO y MAYOR O IGUAL A 0,
    #    tal como exige la restricción del diseño. Si la edad es negativa,
    #    no es numérica o falta algún dato, NO se inserta el registro y se
    #    regresa al formulario. Esto evita guardar datos inválidos o
    #    corruptos en la base de datos.
    # -------------------------------------------------------------------
    if not (nombre_mascota and especie and edad_texto and nombre_propietario and telefono_propietario):
        # Falta al menos un campo obligatorio: no se inserta.
        return redirect(url_for("index"))

    # Se valida que la edad sea un entero válido.
    if not edad_texto.isdigit():
        # isdigit() es False si hay signo '-' o letras,
        # por lo que descarta edades negativas o no numéricas.
        return redirect(url_for("index"))

    edad = int(edad_texto)

    if edad < 0:
        # Doble comprobación defensiva de que la edad no sea negativa.
        return redirect(url_for("index"))

    # Si pasó todas las validaciones, se registra el paciente.
    registrar_paciente(nombre_mascota, especie, edad, nombre_propietario, telefono_propietario)

    # Patrón POST-Redirect-GET: se redirige a la página principal para que,
    # al recargar el navegador, no se reenvíe el formulario por accidente.
    return redirect(url_for("index"))


@app.route("/editar/<int:id_paciente>")
def editar(id_paciente):
    """
    Muestra el formulario de edición (GET) con los datos del paciente
    ya cargados. Si el id no existe, regresa a la lista principal.
    """
    paciente = obtener_paciente(id_paciente)

    if paciente is None:
        # No existe ese paciente: se vuelve a la página principal.
        return redirect(url_for("index"))

    return render_template("editar.html", paciente=paciente)


@app.route("/actualizar/<int:id_paciente>", methods=["POST"])
def actualizar(id_paciente):
    """
    Procesa el formulario de edición (POST) y actualiza los datos
    del paciente. Aplica las MISMAS validaciones que el registro.
    """
    # Se recogen los datos enviados desde el formulario de edición.
    nombre_mascota = request.form.get("nombre_mascota", "").strip()
    especie = request.form.get("especie", "").strip()
    edad_texto = request.form.get("edad", "").strip()
    nombre_propietario = request.form.get("nombre_propietario", "").strip()
    telefono_propietario = request.form.get("telefono_propietario", "").strip()

    # SEGURIDAD 2 (Validación de entradas antes de actualizar en la BD):
    # se reutilizan las mismas reglas que en el registro para no guardar
    # datos vacíos, no numéricos o edades negativas.
    if not (nombre_mascota and especie and edad_texto and nombre_propietario and telefono_propietario):
        return redirect(url_for("editar", id_paciente=id_paciente))

    if not edad_texto.isdigit():
        return redirect(url_for("editar", id_paciente=id_paciente))

    edad = int(edad_texto)

    if edad < 0:
        return redirect(url_for("editar", id_paciente=id_paciente))

    # Si pasó todas las validaciones, se actualiza el paciente.
    actualizar_paciente(id_paciente, nombre_mascota, especie, edad, nombre_propietario, telefono_propietario)

    return redirect(url_for("index"))


@app.route("/eliminar/<int:id_paciente>", methods=["POST"])
def eliminar(id_paciente):
    """
    Elimina un paciente a partir de su id (POST a /eliminar/<id>).

    SEGURIDAD: se usa <int:id_paciente> en la ruta, de modo que Flask solo
    acepta valores enteros para el id. Cualquier otro tipo de dato en la URL
    produce un error 404 y nunca llega a la consulta, reforzando la validación.
    """
    eliminar_paciente(id_paciente)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # debug=True facilita el desarrollo mostrando errores detallados.
    app.run(debug=True)