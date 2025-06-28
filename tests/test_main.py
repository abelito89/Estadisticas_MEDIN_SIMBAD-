"""
Tests para main.py
"""
import pytest
from unittest import mock
import main

def test_main_ok(monkeypatch):
    """Debe imprimir 'Prueba OK' si la conexión y consulta son exitosas."""
    dummy_cursor = mock.Mock()
    dummy_cursor.fetchone.return_value = [1]
    dummy_conn = mock.Mock()
    dummy_conn.cursor.return_value = dummy_cursor
    monkeypatch.setattr(main, "medin_connection", lambda: mock.Mock(__enter__=lambda s: dummy_conn, __exit__=lambda s, a, b, c: None))
    with mock.patch("builtins.print") as mprint:
        main.main()
        mprint.assert_any_call("Prueba OK, DUAL=>", 1)

def test_main_keyerror(monkeypatch):
    """Debe imprimir error de configuración si falta la clave MEDIN."""
    monkeypatch.setattr(main, "medin_connection", lambda: (_ for _ in ()).throw(KeyError))
    with mock.patch("builtins.print") as mprint:
        main.main()
        mprint.assert_any_call("Error: No se encontró la configuración 'MEDIN' en el config manager.")

def test_main_db_error(monkeypatch):
    """Debe imprimir error de conexión si cx_Oracle falla."""
    monkeypatch.setattr(main, "medin_connection", lambda: (_ for _ in ()).throw(Exception("fail")))
    with mock.patch("builtins.print") as mprint:
        main.main()
        # Buscar que se haya impreso el mensaje de error
        found = any(
            call[0][0] == "Error inesperado:" and "fail" in str(call[0][1])
            for call in mprint.call_args_list
        )
        assert found, "No se encontró el mensaje de error esperado en print."
