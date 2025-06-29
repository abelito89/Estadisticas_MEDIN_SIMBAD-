"""
logger_config.py

Función para inicializar logging de forma consistente en toda la aplicación.
"""

import logging
import logging.handlers
from logging import Logger
from pathlib import Path
from typing import Optional

def setup_logging(log_level: int = logging.DEBUG) -> None:
    """
    Inicializa el sistema de logging:
      - Un StreamHandler a consola con nivel INFO+
      - Un FileHandler rotatorio en logs/app.log con nivel DEBUG+

    Llama a esta función al arrancar tu app (una sola vez).
    """
    # 1) Crea carpeta de logs
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # 2) Handlers
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    file = logging.handlers.RotatingFileHandler(
        filename=log_dir / "app.log",
        maxBytes=10*1024*1024,     # 10 MB
        backupCount=5,
        encoding="utf-8"
    )
    file.setLevel(logging.DEBUG)
    file.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    # 3) Configuración global
    root = logging.getLogger()
    root.setLevel(log_level)
    root.addHandler(console)
    root.addHandler(file)

def get_logger(name: Optional[str] = None) -> Logger:
    """
    Devuelve un logger ya configurado.
    Úsalo siempre tras llamar a setup_logging().
    """
    return logging.getLogger(name)