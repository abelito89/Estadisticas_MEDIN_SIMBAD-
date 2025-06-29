"""
Archivo de pruebas automáticas para medin_connection.py

Este archivo contiene tests que aseguran el correcto funcionamiento del context manager para conexiones a la base de datos MEDIN:
- Verifica que se abre y cierra la conexión correctamente con configuración válida.
- Comprueba que se lanza KeyError si falta la configuración.
- Asegura que los errores de base de datos se propagan adecuadamente.

Se utilizan mocks para simular tanto la configuración como la conexión a Oracle, permitiendo pruebas sin acceso real a la base de datos.
"""
import pytest
from src import medin_connection
from unittest import mock
import cx_Oracle


def test_medin_connection_ok(monkeypatch):
    """
    Prueba que el context manager abre y cierra la conexión correctamente cuando la configuración es válida.

    Teoría:
    Un context manager en Python (bloque 'with') se usa para manejar recursos que deben abrirse y cerrarse correctamente, como archivos o conexiones a bases de datos. Aquí, simulamos (mockeamos) la conexión para no depender de una base real.

    ¿Qué hace este test?
    - Simula una conexión a la base de datos usando una clase DummyConn.
    - Simula la función de configuración para que siempre devuelva datos válidos.
    - Simula la función de conexión de cx_Oracle para que devuelva nuestro DummyConn.
    - Usa el context manager y verifica que:
        - Se obtiene la conexión simulada.
        - La conexión no está cerrada dentro del bloque.
        - Al salir del bloque, la conexión se cierra correctamente.
    """
    class DummyConn:
        """
        Clase simulada que representa una conexión a base de datos para pruebas.

        ¿Por qué usar una clase dummy?
        En testing, a veces no queremos depender de recursos reales (como una base de datos),
        así que creamos una clase que imita el comportamiento necesario para la prueba.
        Esta clase tiene los métodos mínimos que se esperan de una conexión real:
        - cursor: devuelve a sí misma para simplificar el test.
        - execute: simula la ejecución de una consulta.
        - fetchone: simula la obtención de un resultado.
        - close: marca la conexión como cerrada.
        """
        def cursor(self): return self
        def execute(self, q): return None
        def fetchone(self): return [1]
        def close(self): self.closed = True
    dummy = DummyConn()
    monkeypatch.setattr(medin_connection, "cargar_configuracion", lambda: {"MEDIN": {"user": "u", "password": "p", "dsn": "d"}})
    monkeypatch.setattr(cx_Oracle, "connect", lambda **kwargs: dummy)
    with medin_connection.medin_connection() as conn:
        assert conn is dummy
        assert not hasattr(dummy, 'closed')  # No debe estar cerrada dentro del with
    assert dummy.closed  # Debe estar cerrada al salir del with


def test_medin_connection_keyerror(monkeypatch):
    """
    Prueba que se lanza un KeyError si la configuración para MEDIN no existe.

    Teoría:
    Cuando se intenta acceder a una clave que no existe en un diccionario en Python, se lanza un KeyError. Aquí simulamos que la configuración no tiene la clave 'MEDIN'.

    ¿Qué hace este test?
    - Simula la función de configuración para que devuelva un diccionario vacío.
    - Intenta abrir la conexión usando el context manager.
    - Verifica que se lanza un KeyError, como se espera en este caso.
    """
    monkeypatch.setattr(medin_connection, "cargar_configuracion", lambda: {})
    with pytest.raises(KeyError):
        with medin_connection.medin_connection():
            pass


def test_medin_connection_db_error(monkeypatch):
    """
    Prueba que se propaga correctamente un error de base de datos (DatabaseError) si cx_Oracle falla al conectar.

    Teoría:
    Cuando ocurre un error al conectar a la base de datos, cx_Oracle lanza una excepción DatabaseError. Es importante que nuestro context manager no oculte este error, sino que lo deje pasar para que el programa pueda manejarlo.

    ¿Qué hace este test?
    - Simula la función de configuración para que devuelva datos válidos.
    - Simula la función de conexión de cx_Oracle para que lance una excepción DatabaseError.
    - Verifica que al intentar abrir la conexión, se lanza la excepción esperada.
    """
    monkeypatch.setattr(medin_connection, "cargar_configuracion", lambda: {"MEDIN": {"user": "u", "password": "p", "dsn": "d"}})
    monkeypatch.setattr(cx_Oracle, "connect", lambda **kwargs: (_ for _ in ()).throw(cx_Oracle.DatabaseError("fail")))
    with pytest.raises(cx_Oracle.DatabaseError):
        with medin_connection.medin_connection():
            pass
