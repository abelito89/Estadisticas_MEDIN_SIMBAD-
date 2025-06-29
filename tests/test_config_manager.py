"""
Archivo de pruebas automáticas para config_manager.py

Este archivo valida el correcto funcionamiento de la gestión de configuración de conexiones a bases de datos:
- Comprueba que se leen correctamente las variables de entorno necesarias para una conexión.
- Verifica que se detectan y reportan variables faltantes.
- Testea que la función principal devuelve la configuración completa para todas las conexiones esperadas.

Se usan mocks para simular variables de entorno y evitar dependencias externas.
"""

import os
import pytest
from db_connections import config_manager
from unittest import mock

def test__leer_vars_ok():
    """
    Prueba que la función _leer_vars devuelve un diccionario válido si todas las variables de entorno existen.

    Teoría:
    En aplicaciones reales, las credenciales y parámetros de conexión suelen almacenarse en variables de entorno por seguridad. Esta función debe leerlas correctamente.

    ¿Qué hace este test?
    - Simula (mockea) las variables de entorno necesarias para una conexión.
    - Llama a la función _leer_vars con un prefijo de prueba.
    - Verifica que el resultado es un diccionario con los valores esperados.
    """
    env = {
        'user_TEST': 'u',
        'password_TEST': 'p',
        'dsn_TEST': 'd',
    }
    with mock.patch.dict(os.environ, env):
        result = config_manager._leer_vars('TEST')
        assert result == {'user': 'u', 'password': 'p', 'dsn': 'd'}

def test__leer_vars_missing():
    """
    Prueba que la función _leer_vars lanza un EnvironmentError si falta alguna variable de entorno.

    Teoría:
    Es importante que la función detecte y reporte cuando falta información crítica para la conexión, evitando errores silenciosos.

    ¿Qué hace este test?
    - Simula las variables de entorno, dejando una vacía.
    - Llama a la función _leer_vars.
    - Verifica que se lanza la excepción esperada.
    """
    env = {
        'user_TEST': 'u',
        'password_TEST': '',
        'dsn_TEST': 'd',
    }
    with mock.patch.dict(os.environ, env):
        with pytest.raises(EnvironmentError):
            config_manager._leer_vars('TEST')

def test_cargar_configuracion(monkeypatch):
    """
    Prueba que la función cargar_configuracion devuelve la configuración de todas las conexiones si existen las variables.

    Teoría:
    La función principal debe ser capaz de construir un diccionario con la configuración de todas las conexiones necesarias para la app, usando los datos de entorno.

    ¿Qué hace este test?
    - Simula el diccionario de variables de entorno para dos conexiones.
    - Llama a la función cargar_configuracion.
    - Verifica que el resultado contiene la configuración correcta para cada conexión.
    """
    env = {
        'user_MEDIN': 'u1', 'password_MEDIN': 'p1', 'dsn_MEDIN': 'd1',
        'user_Simbad': 'u2', 'password_Simbad': 'p2', 'dsn_Simbad': 'd2',
    }
    monkeypatch.setattr(os, 'environ', env)
    conf = config_manager.cargar_configuracion()
    assert conf['MEDIN'] == {'user': 'u1', 'password': 'p1', 'dsn': 'd1'}
    assert conf['Simbad'] == {'user': 'u2', 'password': 'p2', 'dsn': 'd2'}
