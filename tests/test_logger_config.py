"""
Tests para logger_config.py
"""
import os
import logging
import shutil
from config import logger_config
from pathlib import Path

def test_setup_logging_crea_logs():
    """Debe crear la carpeta logs y el archivo app.log al inicializar el logging."""
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
    """Debe devolver un logger configurado."""
    logger_config.setup_logging()
    logger = logger_config.get_logger("test")
    assert isinstance(logger, logging.Logger)
