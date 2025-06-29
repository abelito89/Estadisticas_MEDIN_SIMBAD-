"""
Archivo de pruebas automáticas para logger_config.py

Este archivo verifica que el sistema de logging de la aplicación:
- Crea correctamente la carpeta y el archivo de logs al inicializarse.
- Devuelve un logger configurado y funcional.

Se emplean pruebas que manipulan el sistema de archivos de manera controlada para asegurar que el logging funciona sin errores y no deja residuos.
"""
import os
import logging
import shutil
from config import logger_config
from pathlib import Path

def test_setup_logging_crea_logs():
    """
    Prueba que la función setup_logging crea la carpeta de logs y el archivo app.log al inicializar el logging.

    Teoría:
    El logging es fundamental para registrar eventos y errores en una aplicación. Es importante que el sistema cree correctamente los archivos y carpetas necesarios para guardar los logs.

    ¿Qué hace este test?
    - Elimina la carpeta de logs si existe (limpieza previa).
    - Llama a la función de inicialización de logging.
    - Verifica que la carpeta y el archivo de logs existen.
    - Elimina la carpeta de logs al final (limpieza posterior).
    """
    # Ruta real donde se creará logs
    logs_dir = Path(__file__).parent.parent / "logs"
    # Limpia antes
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
    logger_config.setup_logging()
    assert logs_dir.exists()
    assert (logs_dir / "app.log").exists()
    # Limpia después
    shutil.rmtree(logs_dir)

def test_get_logger():
    """
    Prueba que la función get_logger devuelve un logger configurado y funcional.

    Teoría:
    Un logger es un objeto que permite registrar mensajes en diferentes niveles (info, error, debug, etc). Debe estar correctamente configurado para que la app pueda registrar eventos.

    ¿Qué hace este test?
    - Inicializa el sistema de logging.
    - Obtiene un logger usando la función get_logger.
    - Verifica que el objeto devuelto es una instancia de Logger.
    """
    logger_config.setup_logging()
    logger = logger_config.get_logger("test")
    assert isinstance(logger, logging.Logger)
