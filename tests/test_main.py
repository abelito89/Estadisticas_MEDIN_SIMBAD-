"""
Archivo de pruebas automáticas para main.py

Este archivo contiene tests que simulan distintos escenarios de ejecución del programa principal:
- Verifica que la función main imprime el mensaje correcto cuando la conexión a la base de datos es exitosa.
- Comprueba que se maneja correctamente la ausencia de configuración (KeyError).
- Asegura que los errores inesperados en la conexión se reportan adecuadamente.

Se utilizan técnicas de mocking para simular el comportamiento de la base de datos y la función print, permitiendo probar la lógica sin requerir una base real.
"""

from unittest import mock

import main


def test_main_ok(monkeypatch):
    """
    Prueba que la función main imprime el mensaje correcto cuando la conexión y consulta son exitosas.

    Teoría:
    En testing, muchas veces simulamos (mockeamos) recursos externos para no depender de ellos. Aquí, simulamos la conexión a la base de datos y la función print.

    ¿Qué hace este test?
    - Simula un cursor y una conexión a base de datos.
    - Simula el context manager de conexión.
    - Ejecuta la función main.
    - Verifica que se imprime el mensaje de éxito esperado.
    """
    dummy_cursor = mock.Mock()
    dummy_cursor.fetchone.return_value = [1]
    dummy_conn = mock.Mock()
    dummy_conn.cursor.return_value = dummy_cursor
    monkeypatch.setattr(
        main,
        "medin_connection",
        lambda: mock.Mock(
            __enter__=lambda s: dummy_conn, __exit__=lambda s, a, b, c: None
        ),
    )
    with mock.patch("builtins.print") as mprint:
        main.main()
        mprint.assert_any_call("Prueba OK, DUAL=>", 1)


def test_main_keyerror(monkeypatch):
    """
    Prueba que la función main imprime el mensaje de error adecuado si falta la clave de configuración 'MEDIN'.

    Teoría:
    Cuando falta una clave en la configuración, la función main debe capturar el error y mostrar un mensaje claro al usuario.

    ¿Qué hace este test?
    - Simula que la función de conexión lanza un KeyError.
    - Ejecuta la función main.
    - Verifica que se imprime el mensaje de error esperado.
    """
    monkeypatch.setattr(main, "medin_connection", lambda: (_ for _ in ()).throw(KeyError))
    with mock.patch("builtins.print") as mprint:
        main.main()
        mprint.assert_any_call(
            "Error: No se encontró la configuración 'MEDIN' en el config manager."
        )


def test_main_db_error(monkeypatch):
    """
    Prueba que la función main imprime el mensaje de error adecuado si ocurre un error inesperado en la conexión.

    Teoría:
    Es importante que los errores inesperados se informen claramente al usuario, para facilitar el diagnóstico y la corrección.

    ¿Qué hace este test?
    - Simula que la función de conexión lanza una excepción genérica.
    - Ejecuta la función main.
    - Verifica que se imprime el mensaje de error esperado.
    """
    monkeypatch.setattr(
        main, "medin_connection", lambda: (_ for _ in ()).throw(Exception("fail"))
    )
    with mock.patch("builtins.print") as mprint:
        main.main()
        # Buscar que se haya impreso el mensaje de error
        found = any(
            call[0][0] == "Error inesperado:" and "fail" in str(call[0][1])
            for call in mprint.call_args_list
        )
        assert found, "No se encontró el mensaje de error esperado en print."
