from utiles import establecer_conexion
import json

json_data = {
    "HOST": "postgres-db",
    "USER": "postgres",
    "PASSWORD": "Junio2023+",
    "DATABASE": "itemsdb"
}


conexion = establecer_conexion(json_data)

if conexion is not None:
    print("Conexión establecida correctamente.")
    # Aquí puedes realizar otras operaciones con la conexión a la base de datos
else:
    print("Error al establecer la conexión a la base de datos.")