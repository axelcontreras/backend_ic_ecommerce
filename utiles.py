import json
import psycopg2
import logging

def leer_json(nombre_archivo: str) -> list:
    """Carga la información del archivo JSON como una lista.

    Args:
        nombre_archivo (str): Ruta del archivo en formato JSON.

    Returns:
        list: Lista con los datos cargados desde el archivo JSON.
    """
    try:
        with open(nombre_archivo, 'r') as archivo:
            contenido = archivo.read()
            datos_json = json.loads(contenido)
        return datos_json
    except FileNotFoundError:
        logging.error("Archivo no encontrado:", nombre_archivo)
        return []
    except json.JSONDecodeError as e:
        logging.error("Error al decodificar el archivo JSON:", e)
        return []

def establecer_conexion(json_data: dict) -> psycopg2.extensions.connection:
    """Establece una conexión a la base de datos usando los datos proporcionados en formato JSON.

    Args:
        json_data (dict): Datos de conexión en formato JSON.

    Returns:
        psycopg2.extensions.connection: Objeto de conexión a la base de datos.
    """    
    try:
        conexion = psycopg2.connect(
            host=json_data["HOST"],
            user=json_data["USER"],
            password=json_data["PASSWORD"],
            dbname=json_data["DATABASE"]
        )
        logging.info("Conexión establecida correctamente.")
        return conexion
    except psycopg2.Error as e:
        logging.error(f"Error al establecer la conexión a la base de datos: {e}")
        return None

def verificar_conexion(conexion: psycopg2.extensions.connection):
    """Verifica si la conexión a la base de datos es válida.

    Args:
        conexion (psycopg2.extensions.connection): Objeto de conexión a la base de datos.
    """    
    if conexion is not None:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT 1")
            resultado = cursor.fetchone()
            if resultado[0] == 1:
                logging.info("La conexión es válida.")
            else:
                logging.info("La conexión es inválida.")
        except psycopg2.Error as e:
            logging.error(f"Error al verificar la conexión a la base de datos: {e}")
        finally:
            cursor.close()
    else:
        logging.info("No se ha establecido una conexión válida.")

def ejecutar_consulta(consulta: str):
    """Ejecuta una consulta en la base de datos.

    Args:
        consulta (str): Consulta SQL a ejecutar.
    """
    try:
        json_data = leer_json("conf/database.json")
        conexion = establecer_conexion(json_data)
        cursor = conexion.cursor()

        cursor.execute(consulta)

        conexion.commit()
        cursor.close()
        conexion.close()
        logging.info("Consulta ejecutada correctamente.")
    except psycopg2.Error as e:
        logging.error("Error al ejecutar la consulta:", e)

def obtener_items_disponibles():
    """Obtiene todos los items disponibles de la base de datos.

    Returns:
        list: Lista de diccionarios que representan los items.
    """
    json_data = leer_json("conf/database.json")
    conexion = establecer_conexion(json_data)
    if conexion is not None:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM items")
                columnas = [desc[0] for desc in cursor.description]
                resultados = cursor.fetchall()
                items = []
                for resultado in resultados:
                    item = dict(zip(columnas, resultado))
                    items.append(item)
                return items
        except psycopg2.Error as e:
            logging.error(f"Error al obtener los items disponibles: {e}")
        finally:
            conexion.close()
    else:
        return None

def obtener_item_por_codigo(codigo):
    """Obtiene un item de la base de datos por su código.

    Args:
        codigo: Código del item a obtener.

    Returns:
        dict: Diccionario que representa el item.
    """
    json_data = leer_json("conf/database.json")
    conexion = establecer_conexion(json_data)
    if conexion is not None:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM items WHERE codigo = %s", (codigo,))
                columnas = [desc[0] for desc in cursor.description]
                resultado = cursor.fetchone()
                if resultado:
                    item = dict(zip(columnas, resultado))
                    return item
                else:
                    logging.info("No se encontró ningún item con el código especificado.")
                    return None
        except psycopg2.Error as e:
            logging.error(f"Error al obtener el item por código: {e}")
        finally:
            conexion.close()
    else:
        return None

def crear_item(nombre, talla, color, precio, cantidad, imagen):
    """Crea un nuevo item en la base de datos.

    Args:
        nombre (str): Nombre del item.
        talla (str): Talla del item.
        color (str): Color del item.
        precio (float): Precio del item.
        cantidad (int): Cantidad disponible del item.
        imagen (str): Ruta de la imagen del item.
    """
    json_data = leer_json("conf/database.json")
    conexion = establecer_conexion(json_data)
    if conexion is not None:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO items (nombre, talla, color, precio, cantidad, imagen)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nombre, talla, color, precio, cantidad, imagen))
            conexion.commit()
            logging.info("El item ha sido creado correctamente.")
        except psycopg2.Error as e:
            logging.error(f"Error al crear el item: {e}")
        finally:
            conexion.close()

def modificar_item(codigo, nombre, talla, color, precio, cantidad, imagen):
    """Modifica un item existente en la base de datos.

    Args:
        codigo: Código del item a modificar.
        nombre (str): Nuevo nombre del item.
        talla (str): Nueva talla del item.
        color (str): Nuevo color del item.
        precio (float): Nuevo precio del item.
        cantidad (int): Nueva cantidad disponible del item.
        imagen (str): Nueva ruta de la imagen del item.
    """
    json_data = leer_json("conf/database.json")
    conexion = establecer_conexion(json_data)
    if conexion is not None:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    UPDATE items
                    SET nombre = %s, talla = %s, color = %s, precio = %s, cantidad = %s, imagen = %s
                    WHERE codigo = %s
                """, (nombre, talla, color, precio, cantidad, imagen, codigo))
            conexion.commit()
            logging.info("El item ha sido modificado correctamente.")
        except psycopg2.Error as e:
            logging.error(f"Error al modificar el item: {e}")
        finally:
            conexion.close()

def eliminar_item(codigo):
    """Elimina un item de la base de datos por su código.

    Args:
        codigo: Código del item a eliminar.
    """
    json_data = leer_json("conf/database.json")
    conexion = establecer_conexion(json_data)
    if conexion is not None:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM items WHERE codigo = %s", (codigo,))
            conexion.commit()
            logging.info("El item ha sido eliminado correctamente.")
        except psycopg2.Error as e:
            logging.error(f"Error al eliminar el item: {e}")
        finally:
            conexion.close()
