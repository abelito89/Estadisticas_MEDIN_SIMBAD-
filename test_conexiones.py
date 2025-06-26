import cx_Oracle
from db_connections.config_manager import cargar_configuracion

def probar_conexion(nombre, conf):
    conn = cx_Oracle.connect(
        user=conf['user'],
        password=conf['password'],
        dsn=conf['dsn'],
        encoding="UTF-8",     # opcional
        nencoding="UTF-8"
    )
    print(f"✅ {nombre}: versión {conn.version}")
    conn.close()

if __name__ == "__main__":
    for nombre, conf in cargar_configuracion().items():
        try:
            probar_conexion(nombre, conf)
        except Exception as e:
            print(f"❌ {nombre}: {e}")
