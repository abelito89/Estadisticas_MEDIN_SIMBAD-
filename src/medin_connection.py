from typing import Generator
from contextlib import contextmanager

import cx_Oracle
from db_connections.config_manager import cargar_configuracion


@contextmanager
def medin_connection() -> Generator[cx_Oracle.Connection, None, None]:
    """
    Context manager para gestionar de forma segura conexiones a la base de datos MEDIN.

    Este context manager se encarga de:
      1. Cargar la configuración (usuario, contraseña, DSN) mediante `cargar_configuracion()`.
      2. Abrir una conexión con cx_Oracle.
      3. Entregarla al bloque `with`.
      4. Cerrar la conexión automáticamente al salir del bloque, ocurra o no una excepción.

    Ejemplo de uso:
        with medin_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tabla_ejemplo")
            for fila in cursor:
                print(fila)

    Yields:
        cx_Oracle.Connection:
            Objeto de conexión abierto y listo para ejecutar consultas.

    Raises:
        KeyError:
            Si la clave "MEDIN" no existe en el diccionario de configuración.
        cx_Oracle.DatabaseError:
            Si ocurre un error al intentar establecer la conexión (credenciales inválidas, DSN incorrecto, etc.).

    """
    dict_configuraciones = cargar_configuracion()
    # Extraemos el sub-diccionario para la base MEDIN; puede lanzar KeyError
    conf_medin = dict_configuraciones["MEDIN"]

    conn: cx_Oracle.Connection | None = None
    try:
        conn = cx_Oracle.connect(
            user=conf_medin["user"],
            password=conf_medin["password"],
            dsn=conf_medin["dsn"],
        )
        yield conn
    finally:
        # Cerramos la conexión solo si se abrió correctamente
        if conn:
            conn.close()

    

    
