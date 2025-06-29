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
  python test_conexiones.py
  ```
- Para ejecutar la aplicación principal:
  ```bash
  python main.py
  ```

## Estructura del proyecto
- `src/` Código principal de conexión y lógica
- `db_connections/` Gestión de configuración y utilidades de conexión
- `config/` Configuración de logging
- `test_conexiones.py` Script para probar conexiones
- `.env.example` Plantilla de variables de entorno

## Notas
- No subas tu archivo `.env` real al repositorio.
- El directorio `logs/` se crea automáticamente al ejecutar la app.

## Licencia
(Sin licencia definida, agregar si es necesario)
