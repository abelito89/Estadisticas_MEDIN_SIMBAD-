from src.medin_connection import medin_connection
import cx_Oracle


def main():
    try:
        with medin_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            resultado = cursor.fetchone()
            print("Prueba OK, DUAL=>", resultado[0])
    except KeyError:
        print("Error: No se encontró la configuración 'MEDIN' en el config manager.")
    except cx_Oracle.DatabaseError as db_err:
        print("Error de conexión a Oracle:", db_err)
    except Exception as exc:
        print("Error inesperado:", exc)

    except Exception as e:
        pass



if __name__ == "__main__":
    main()