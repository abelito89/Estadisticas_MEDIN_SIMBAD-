# Estadísticas MEDIN/SIMBAD

Este proyecto permite gestionar y consultar estadísticas diarias de las bases de datos MEDIN y Simbad mediante conexiones Oracle.

## Requisitos
- Python 3.8+
- Oracle Client (para cx_Oracle)
- Variables de entorno configuradas (ver `.env.example`)

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/abelito89/Estadisticas_MEDIN_SIMBAD-.git
   cd Estadisticas_MEDIN_SIMBAD-
   ```
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Copia el archivo `.env.example` a `.env` y completa tus credenciales:
   ```bash
   cp .env.example .env
   # Edita .env con tus datos
   ```

## Uso
- Para probar la conexión a las bases de datos:
  ```bash
  python main.py
  ```
- Para ejecutar la aplicación principal:
  ```bash
  python main.py
  ```
- Para ejecutar los tests automáticos:
  ```bash
  pytest
  ```

## Variables de entorno
El archivo `.env` debe contener las credenciales de las bases de datos. Ejemplo:
```env
user_MEDIN=usuario_medin
password_MEDIN=contraseña_medin
dsn_MEDIN=dsn_medin
user_Simbad=usuario_simbad
password_Simbad=contraseña_simbad
dsn_Simbad=dsn_simbad
```

## Logging
El sistema de logging se configura automáticamente al iniciar la aplicación:
- Los logs se almacenan en `logs/app.log` (rotativo, hasta 5 archivos de 10MB).
- También se muestran en consola.
- Puedes personalizar el nivel de logging en `config/logger_config.py`.

## Estructura del proyecto
- `src/` Código principal de conexión y lógica (ej: `medin_connection.py`)
- `db_connections/` Gestión de configuración y utilidades de conexión (`config_manager.py`)
- `config/` Configuración de logging (`logger_config.py`)
- `tests/` Pruebas automáticas con pytest
- `.env.example` Plantilla de variables de entorno
- `logs/` Carpeta de logs (se crea automáticamente)

## Buenas prácticas
- No subas tu archivo `.env` real al repositorio.
- Usa un entorno virtual para aislar dependencias.
- Los tests usan mocks para no requerir bases de datos reales.
- El código está modularizado para facilitar el mantenimiento y la extensión.

## Dependencias principales
- `cx_Oracle`: Conexión a bases de datos Oracle
- `python-dotenv`: Carga de variables de entorno
- `pytest`: Testing automático

## Licencia
(Sin licencia definida, agregar si es necesario)
