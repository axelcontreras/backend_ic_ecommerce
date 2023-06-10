# README

Este proyecto contiene un conjunto de funciones para interactuar con una base de datos PostgreSQL y realizar operaciones CRUD en una tabla llamada "items". El código está escrito en Python y utiliza la librería psycopg2 para establecer la conexión con la base de datos.

## Estructura del proyecto

El proyecto tiene la siguiente estructura de archivos:

- `utiles.py`: Archivo principal que contiene las funciones para interactuar con la base de datos.
- `conf/database.json`: Archivo de configuración en formato JSON que almacena los datos de conexión a la base de datos.
- `test_utiles.py`: Archivo de pruebas unitarias para verificar el funcionamiento de las funciones en `utiles.py`.
- `README.md`: Este archivo que proporciona información sobre el proyecto.
- `requirements.txt`: Archivo que especifica las dependencias del proyecto.

## Requisitos

- Python 3.x
- Librería psycopg2

## Configuración

Antes de ejecutar el código, asegúrate de configurar correctamente los datos de conexión a la base de datos PostgreSQL en el archivo `conf/database.json`. El archivo debe seguir el siguiente formato:

```json
{
  "HOST": "nombre_del_host",
  "USER": "nombre_de_usuario",
  "PASSWORD": "contraseña",
  "DATABASE": "nombre_de_la_base_de_datos"
}
```

Reemplaza los valores `nombre_del_host`, `nombre_de_usuario`, `contraseña` y `nombre_de_la_base_de_datos` con tus propios datos de conexión.

Además, asegúrate de tener las dependencias requeridas instaladas. Puedes instalarlas ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
```

Claro, aquí tienes la sección adicional para el README:

## Creación de la base de datos y usuario

Si deseas crear una base de datos llamada "itemsDB" con un usuario "postgres" y sin contraseña, puedes seguir los siguientes pasos:

1. Asegúrate de tener PostgreSQL instalado en tu sistema. Puedes descargarlo desde el sitio oficial de PostgreSQL (https://www.postgresql.org) e instalarlo siguiendo las instrucciones proporcionadas para tu sistema operativo.

2. Una vez instalado, abre una terminal o consola de comandos y asegúrate de que el comando `psql` esté disponible. Puedes verificarlo ejecutando el siguiente comando:

   ```bash
   psql --version
   ```

   Si el comando es reconocido y se muestra la versión de PostgreSQL, esta listo para continuar. De lo contrario, asegúrate de haber agregado la ubicación del ejecutable `psql` al PATH del sistema.

3. Conecta con el usuario predeterminado "postgres" ejecutando el siguiente comando:

   ```bash
   psql -U postgres
   ```

   Si esta en Windows y no tienes una contraseña establecida para el usuario "postgres", puedes usar el siguiente comando:

   ```bash
   psql -U postgres -w
   ```

   Esto te permitirá conectarte sin solicitar una contraseña.

4. Una vez conectado, ejecuta el siguiente comando para crear la base de datos "itemsDB":

   ```bash
   CREATE DATABASE itemsDB;
   ```

5. A continuación, crea un usuario llamado "postgres" y asígnale los permisos necesarios para acceder a la base de datos "itemsDB":

   ```bash
   CREATE USER postgres WITH PASSWORD '';
   GRANT ALL PRIVILEGES ON DATABASE itemsDB TO postgres;
   ```

   Tenga en cuenta que el segundo comando establece una contraseña vacía para el usuario "postgres". Si deseas establecer una contraseña diferente, reemplaza las comillas vacías con tu contraseña elegida.

6. ¡Listo! Ahora tienes la base de datos "itemsDB" y el usuario "postgres" configurados. Asegúrate de utilizar estos detalles de conexión en el archivo `conf/database.json` del proyecto:

   ```json
   {
     "HOST": "localhost",
     "USER": "postgres",
     "PASSWORD": "",
     "DATABASE": "itemsDB"
   }
   ```

   Asegúrate de que el archivo `conf/database.json` esté correctamente configurado antes de ejecutar el código.

Recuerda que estos pasos son una guía básica para crear una base de datos y un usuario en PostgreSQL. Si necesitas una configuración más avanzada o específica, consulta la documentación oficial de PostgreSQL o busca recursos adicionales en línea.


## Uso

Puedes utilizar las siguientes funciones en `utiles.py` para interactuar con la base de datos:

- `obtener_items_disponibles()`: Obtiene todos los items disponibles de la base de datos y devuelve una lista de diccionarios.
- `obtener_item_por_codigo(codigo)`: Obtiene un item de la base de datos por su código y devuelve un diccionario que representa el item.
- `crear_item(nombre, talla, color, precio, cantidad, imagen)`: Crea un nuevo item en la base de datos.
- `modificar_item(codigo, nombre, talla, color, precio, cantidad, imagen)`: Modifica un item existente en la base de datos.
- `eliminar_item(codigo)`: Elimina un item de la base de datos por su código.

Puedes utilizar el archivo `test_utiles.py` para ejecutar pruebas unitarias y verificar el correcto funcionamiento de las funciones.

## Ejecución

Para ejecutar el código, simplemente ejecuta el archivo `utiles.py`:

```bash
python utiles.py
```

Recuerda tener la configuración de la base de datos correctamente establecida antes de ejecutar el código.

## Pruebas

El proyecto cuenta con pruebas unitarias para verificar el correcto funcionamiento de las funciones implementadas. Estas pruebas se encuentran en el archivo `test_utiles.py`.

### Ejecución de las pruebas

Para ejecutar las pruebas, asegúrate de tener el entorno configurado y las dependencias instaladas. Luego, puedes ejecutar el siguiente comando:

```bash
python test_utiles.py
```

Asegúrate de encontrarte en el directorio raíz del proyecto al ejecutar el comando.

El archivo `test_utiles

.py` contiene las siguientes pruebas:

1. `test_1_crear_item`: Verifica la creación de un nuevo item en la base de datos.
2. `test_2_crear_items`: Verifica la creación de varios items en la base de datos.
3. `test_3_modificar_item`: Verifica la modificación de un item existente en la base de datos.
4. `test_4_obtener_items_disponibles`: Verifica la obtención de todos los items disponibles en la base de datos.
5. `test_5_obtener_item_por_codigo`: Verifica la obtención de un item específico por su código.
6. `test_6_eliminar_item`: Verifica la eliminación de un item de la base de datos.

Cada prueba realiza las operaciones correspondientes y verifica los resultados esperados utilizando los métodos y funciones implementados en el script principal.

Tenga en cuenta que estas pruebas asumen que se han configurado correctamente los datos de conexión a la base de datos en el archivo `conf/database.json`. Asegúrese de proporcionar los datos correctos antes de ejecutar las pruebas.

```
Recuerda que el archivo `requirements.txt` debe contener las dependencias necesarias para el proyecto. Asegúrate de incluir todas las dependencias y versiones específicas que requieras.