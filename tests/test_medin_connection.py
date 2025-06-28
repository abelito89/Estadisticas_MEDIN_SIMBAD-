"""
Tests para medin_connection.py
"""
import pytest
from src import medin_connection
from unittest import mock
import cx_Oracle

def test_medin_connection_ok(monkeypatch):
    """Debe abrir y cerrar la conexión correctamente si la config es válida."""
    class DummyConn:
        def cursor(self): return self
        def execute(self, q): return None
        def fetchone(self): return [1]
        def close(self): self.closed = True
    dummy = DummyConn()
    monkeypatch.setattr(medin_connection, "cargar_configuracion", lambda: {"MEDIN": {"user": "u", "password": "p", "dsn": "d"}})
    monkeypatch.setattr(cx_Oracle, "connect", lambda **kwargs: dummy)
    with medin_connection.medin_connection() as conn:
        assert conn is dummy
        assert not hasattr(dummy, 'closed')
    assert dummy.closed

def test_medin_connection_keyerror(monkeypatch):
    """Debe lanzar KeyError si no existe la config MEDIN."""
    monkeypatch.setattr(medin_connection, "cargar_configuracion", lambda: {})
    with pytest.raises(KeyError):
        with medin_connection.medin_connection():
            pass

def test_medin_connection_db_error(monkeypatch):
    """Debe propagar DatabaseError si cx_Oracle falla."""
    monkeypatch.setattr(medin_connection, "cargar_configuracion", lambda: {"MEDIN": {"user": "u", "password": "p", "dsn": "d"}})
    class DummyDBError(Exception): pass
    monkeypatch.setattr(cx_Oracle, "connect", lambda **kwargs: (_ for _ in ()).throw(cx_Oracle.DatabaseError("fail")))
    with pytest.raises(cx_Oracle.DatabaseError):
        with medin_connection.medin_connection():
            pass
