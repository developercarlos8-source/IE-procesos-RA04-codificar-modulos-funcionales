# database.py
# Responsable de crear la base de datos y la tabla 'pacientes'.

import sqlite3

# Nombre del archivo de base de datos SQLite
NOMBRE_BD = "patitassanas.db"


def obtener_conexion():
    """
    Crea y devuelve una conexión a la base de datos SQLite.
    row_factory = sqlite3.Row permite acceder a las columnas por su nombre
    (por ejemplo: paciente['nombre_mascota']), lo que hace el código más legible.
    """
    conexion = sqlite3.connect(NOMBRE_BD)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_bd():
    """
    Crea la tabla 'pacientes' si aún no existe.

    SEGURIDAD / ROBUSTEZ: se usa 'CREATE TABLE IF NOT EXISTS' para que, al
    ejecutar el proyecto varias veces, la tabla NO se duplique ni genere error.

    Además se aplica la restricción CHECK (edad >= 0) directamente en la base
    de datos: esto es una segunda barrera de validación, por si algún dato
    intentara insertarse saltándose la validación de la aplicación.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_mascota       TEXT    NOT NULL,
            especie              TEXT    NOT NULL,
            edad                 INTEGER NOT NULL CHECK (edad >= 0),
            nombre_propietario   TEXT    NOT NULL,
            telefono_propietario TEXT    NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


# Permite crear la base de datos ejecutando directamente: python database.py
if __name__ == "__main__":
    inicializar_bd()
    print("Base de datos 'patitassanas.db' y tabla 'pacientes' creadas correctamente.")