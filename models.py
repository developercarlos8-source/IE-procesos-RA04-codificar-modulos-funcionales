# models.py
# Contiene las funciones CRUD (Crear, Leer, Actualizar, Eliminar)
# sobre la tabla 'pacientes'. Aquí vive la lógica de acceso a datos.

from database import obtener_conexion


def registrar_paciente(nombre_mascota, especie, edad, nombre_propietario, telefono_propietario):
    """
    CRUD -> C (Create): inserta un nuevo paciente en la base de datos.

    SEGURIDAD 1 (Anti inyección SQL): se usan CONSULTAS PARAMETRIZADAS.
    Los valores del formulario NO se concatenan en la cadena SQL; se envían
    aparte mediante los marcadores de posición (?) y una tupla de parámetros.
    Así, aunque el usuario escriba texto malicioso, SQLite lo trata como
    dato y nunca como instrucción SQL ejecutable.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO pacientes
            (nombre_mascota, especie, edad, nombre_propietario, telefono_propietario)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nombre_mascota, especie, edad, nombre_propietario, telefono_propietario)
    )

    conexion.commit()
    conexion.close()


def listar_pacientes():
    """
    CRUD -> R (Read): devuelve la lista de todos los pacientes registrados,
    ordenados por id ascendente para que la tabla se muestre de forma coherente.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM pacientes ORDER BY id ASC")
    pacientes = cursor.fetchall()

    conexion.close()
    return pacientes


def obtener_paciente(id_paciente):
    """
    CRUD -> R (Read de un solo registro): devuelve un paciente por su id,
    o None si no existe. Se usa para cargar sus datos en el formulario de edición.

    SEGURIDAD (Anti inyección SQL): consulta parametrizada con (?) para el id.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id_paciente,))
    paciente = cursor.fetchone()

    conexion.close()
    return paciente


def eliminar_paciente(id_paciente):
    """
    CRUD -> D (Delete): elimina un paciente a partir de su id.

    SEGURIDAD (Anti inyección SQL): también aquí se usa una consulta
    parametrizada (?) para el id, en lugar de concatenar el valor recibido.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))

    conexion.commit()
    conexion.close()


def actualizar_paciente(id_paciente, nombre_mascota, especie, edad, nombre_propietario, telefono_propietario):
    """
    CRUD -> U (Update): actualiza los datos de un paciente existente.

    SEGURIDAD (Anti inyección SQL): consulta parametrizada con (?) para
    todos los valores, incluido el id.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE pacientes
        SET nombre_mascota = ?, especie = ?, edad = ?,
            nombre_propietario = ?, telefono_propietario = ?
        WHERE id = ?
        """,
        (nombre_mascota, especie, edad, nombre_propietario, telefono_propietario, id_paciente)
    )

    conexion.commit()
    conexion.close()