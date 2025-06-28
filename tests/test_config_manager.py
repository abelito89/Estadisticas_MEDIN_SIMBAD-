"""
Tests para config_manager.py
"""
import os
import pytest
from db_connections import config_manager
from unittest import mock

def test__leer_vars_ok():
    """Debe devolver un diccionario válido si todas las variables existen."""
    env = {
        'user_TEST': 'u',
        'password_TEST': 'p',
        'dsn_TEST': 'd',
    }
    with mock.patch.dict(os.environ, env):
        result = config_manager._leer_vars('TEST')
        assert result == {'user': 'u', 'password': 'p', 'dsn': 'd'}

def test__leer_vars_missing():
    """Debe lanzar EnvironmentError si falta alguna variable."""
    env = {
        'user_TEST': 'u',
        'password_TEST': '',
        'dsn_TEST': 'd',
    }
    with mock.patch.dict(os.environ, env):
        with pytest.raises(EnvironmentError):
            config_manager._leer_vars('TEST')

def test_cargar_configuracion(monkeypatch):
    """Debe devolver la configuración de todas las conexiones si existen las variables."""
    env = {
        'user_MEDIN': 'u1', 'password_MEDIN': 'p1', 'dsn_MEDIN': 'd1',
        'user_Simbad': 'u2', 'password_Simbad': 'p2', 'dsn_Simbad': 'd2',
    }
    monkeypatch.setattr(os, 'environ', env)
    conf = config_manager.cargar_configuracion()
    assert conf['MEDIN'] == {'user': 'u1', 'password': 'p1', 'dsn': 'd1'}
    assert conf['Simbad'] == {'user': 'u2', 'password': 'p2', 'dsn': 'd2'}
