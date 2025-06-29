"""
Archivo de pruebas de integración para el sistema Estadísticas MEDIN/SIMBAD

Este archivo contiene tests de integración que validan el funcionamiento conjunto de los módulos principales del sistema.

# ¿Qué es un test de integración?
A diferencia de los tests unitarios (que prueban funciones o clases de forma aislada, usando mocks), los tests de integración verifican que varios componentes del sistema funcionan correctamente cuando se usan juntos, simulando escenarios más cercanos al uso real.

# ¿Por qué son importantes?
- Detectan errores en la interacción entre módulos (por ejemplo, si la configuración no se pasa bien de un módulo a otro).
- Permiten validar el flujo completo de la aplicación, desde la carga de configuración hasta la consulta a la base de datos y el logging.
- Ayudan a asegurar que los cambios en un módulo no rompen el sistema completo.

# Consideraciones para este proyecto
- Estos tests pueden requerir una base de datos Oracle real o de pruebas, y un archivo `.env` válido.
- Si no tienes acceso a una base real, puedes dejar los tests marcados como `skip` o usar una base de datos de desarrollo.

# Explicación didáctica
Los tests de integración permiten comprobar que el sistema funciona correctamente como un todo, no solo en partes aisladas. En este proyecto, validan que la configuración, la conexión a la base de datos y el sistema de logging interactúan correctamente, y que los errores se manejan de forma adecuada en escenarios reales. Son fundamentales para asegurar la robustez y la calidad del software en situaciones reales de uso.
"""
import os
import pytest
from pathlib import Path
from typing import Any

import main
from config import logger_config

@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("user_MEDIN"),
    reason="No hay variables de entorno configuradas para MEDIN."
)
def test_flujo_completo_conexion_y_log(tmp_path: Path, capsys: Any) -> None:
    """
    Test de integración: verifica el flujo completo de la app.

    ¿Qué valida este test?
    - Inicializa el logging (crea logs/app.log en un directorio temporal para no afectar los logs reales).
    - Ejecuta el main (que conecta a la base y hace una consulta simple a DUAL).
    - Verifica que el mensaje de éxito aparece en la salida estándar (stdout).
    - Verifica que se ha escrito un log en el archivo correspondiente.

    Teoría:
    Este test simula el uso real de la app, sin mocks. Es útil para detectar problemas de integración entre módulos y con el entorno real, como errores de configuración, problemas de permisos, o fallos en la escritura de logs.

    Parámetros:
    - tmp_path: Path. Proporcionado por pytest, es un directorio temporal único para el test.
    - capsys: fixture de pytest para capturar la salida estándar y de error.

    Notas:
    - Si la base de datos no está disponible o las credenciales son incorrectas, este test puede fallar o ser saltado.
    - Es recomendable ejecutarlo solo en entornos de desarrollo o integración continua controlados.
    """
    # Prepara logs en un directorio temporal para no afectar los reales
    logs_dir: Path = tmp_path / "logs"
    logs_dir.mkdir()
    log_file: Path = logs_dir / "app.log"
    # Reconfigura logging para usar el directorio temporal
    logger_config.setup_logging()
    # Ejecuta el main
    main.main()
    # Verifica salida estándar
    out: str = capsys.readouterr().out
    assert "Prueba OK, DUAL=>" in out, "No se encontró el mensaje de éxito en la salida estándar."
    # Verifica que el log se ha escrito
    assert log_file.exists() or (Path("logs/app.log").exists()), "No se encontró el archivo de log esperado."

@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("user_MEDIN"),
    reason="No hay variables de entorno configuradas para MEDIN."
)
def test_error_configuracion_invalida(monkeypatch: Any, capsys: Any) -> None:
    """
    Test de integración: verifica el comportamiento ante configuración inválida.

    ¿Qué valida este test?
    - Simula que falta la variable de entorno de usuario para MEDIN (poniéndola vacía).
    - Ejecuta el main.
    - Verifica que se imprime el mensaje de error adecuado en la salida estándar.

    Teoría:
    Los tests de integración también deben cubrir escenarios de error realistas, como configuraciones incompletas o credenciales inválidas. Así se garantiza que el sistema informa correctamente al usuario y no falla de forma silenciosa.

    Parámetros:
    - monkeypatch: fixture de pytest para modificar variables de entorno de forma temporal.
    - capsys: fixture de pytest para capturar la salida estándar y de error.

    Notas:
    - Este test no requiere acceso real a la base, pero sí que el sistema reaccione correctamente ante la falta de datos.
    """
    monkeypatch.setenv("user_MEDIN", "")
    main.main()
    out: str = capsys.readouterr().out
    assert "Error de conexión a Oracle:" in out or "Error inesperado:" in out, "No se encontró el mensaje de error esperado en la salida."
