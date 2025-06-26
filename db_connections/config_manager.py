"""
Módulo para gestión de configuración de bases de datos Oracle
Lee parámetros de conexión desde variables de entorno (.env)
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any

# Cargar variables de entorno desde .env en el directorio raíz
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def cargar_configuracion() -> Dict[str, Dict[str, Any]]:
    """
    Carga configuraciones de conexión desde variables de entorno
    
    Returns:
        Dict: Configuraciones de bases de datos con estructura:
            {
                'DB_ANTIGUA_1': {
                    'user': ...,
                    'password': ...,
                    'dsn': ...,
                    'encoding': ...,
                },
                ...
            }
    
    Raises:
        EnvironmentError: Si faltan variables críticas
    """
    config = {}
    
    # Configuración para primera base de datos
    db1_config = {
        'user': os.getenv("DB_ANTIGUA_1_USER"),
        'password': os.getenv("DB_ANTIGUA_1_PASSWORD"),
        'dsn': os.getenv("DB_ANTIGUA_1_DSN"),
        'encoding': os.getenv("DB_ANTIGUA_1_ENCODING", "UTF-8")  # Valor por defecto
    }
    
    # Configuración para segunda base de datos
    db2_config = {
        'user': os.getenv("DB_ANTIGUA_2_USER"),
        'password': os.getenv("DB_ANTIGUA_2_PASSWORD"),
        'dsn': os.getenv("DB_ANTIGUA_2_DSN"),
        'encoding': os.getenv("DB_ANTIGUA_2_ENCODING", "UTF-8")
    }
    
    # Validar configuraciones esenciales
    for db_name, config_data in [('DB_ANTIGUA_1', db1_config), ('DB_ANTIGUA_2', db2_config)]:
        if not all([config_data['user'], config_data['password'], config_data['dsn']]):
            raise EnvironmentError(f"Faltan variables de entorno para {db_name}")
    
    config['DB_ANTIGUA_1'] = db1_config
    config['DB_ANTIGUA_2'] = db2_config
    
    return config