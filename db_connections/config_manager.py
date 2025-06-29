"""
config_manager.py

Módulo de gestión de configuración de múltiples conexiones a bases de datos Oracle.
Lee parámetros de conexión desde un archivo .env ubicado en la raíz del proyecto.

Funciones principales:
- cargar_configuracion(): Devuelve un diccionario con las configuraciones de conexión.
- _leer_vars(prefijo): Lee y valida las variables de entorno para un prefijo dado.

Uso:
    from db_connections.config_manager import cargar_configuracion
    config = cargar_configuracion()
    # config['MEDIN'] -> credenciales de MEDIN
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any

# ----------------------------------------
# 1. Carga de variables de entorno
# ----------------------------------------
# Asume que el .env está un nivel por encima de este archivo (en la raíz del proyecto)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# ----------------------------------------
# 2. Función auxiliar
# ----------------------------------------
def _leer_vars(prefijo: str) -> Dict[str, str]:
    """
    Lee y valida las variables de entorno para un prefijo dado.

    Cada conexión espera las variables:
        user_{PREFIJO}
        password_{PREFIJO}
        dsn_{PREFIJO}

    Args:
        prefijo (str): Sufijo que identifica el bloque de variables
                        (por ejemplo, 'MEDIN' o 'Simbad').

    Returns:
        Dict[str, str]: Diccionario con las claves 'user', 'password' y 'dsn'.

    Raises:
        EnvironmentError: Si falta alguna de las variables esperadas.
    """
    # Nombres de las claves a leer
    claves = ["user", "password", "dsn"]
    # Construye un dict { 'user': os.getenv("user_PREFIJO"), ... }
    valores = {k: os.getenv(f"{k}_{prefijo}") for k in claves}

    # Detecta claves faltantes
    faltantes = [k for k, v in valores.items() if not v]
    if faltantes:
        raise EnvironmentError(f"Faltan variables {faltantes} para '{prefijo}'")

    return valores


# ----------------------------------------
# 3. Función pública
# ----------------------------------------
def cargar_configuracion() -> Dict[str, Dict[str, Any]]:
    """
    Construye y devuelve la configuración de todas las conexiones configuradas.

    Utiliza _leer_vars() para cada base de datos que queramos exponer.

    Returns:
        Dict[str, Dict[str, Any]]: Mapeo de nombre de conexión a sus credenciales,
                                   ej. { 'MEDIN': {...}, 'Simbad': {...} }.

    Raises:
        EnvironmentError: Si la lectura de variables falla en alguna conexión.
    """
    return {
        "MEDIN": _leer_vars("MEDIN"),
        "Simbad": _leer_vars("Simbad"),
    }
