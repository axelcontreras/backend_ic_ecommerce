import unittest
from utiles import leer_json, ejecutar_consulta, establecer_conexion, verificar_conexion, crear_item, eliminar_item, modificar_item, obtener_items_disponibles, obtener_item_por_codigo


class TestScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Establecer conexión a la base de datos
        json_data = leer_json("conf/database.json")
        cls.conexion = establecer_conexion(json_data)
        verificar_conexion(cls.conexion)
        # Eliminar la tabla de items antes de cada prueba
        query_drop = "DROP TABLE IF EXISTS items"
        ejecutar_consulta(query_drop)
        # Crear una nueva tabla de items
        query_create = "CREATE TABLE IF NOT EXISTS items (codigo SERIAL PRIMARY KEY, nombre VARCHAR(100), talla VARCHAR(20), color VARCHAR(50), precio NUMERIC(18, 2), cantidad INTEGER, imagen VARCHAR(200), categoria VARCHAR(20), valoracion NUMERIC(3, 2))"
        ejecutar_consulta(query_create)

    @classmethod
    def tearDownClass(cls):
        # Cerrar conexión a la base de datos
        cls.conexion.close()

    def test_1_crear_item(self):
        nuevo_item = {
            "nombre": "Nuevo Item 1",
            "talla": "M",
            "color": "Rojo",
            "precio": 19.99,
            "cantidad": 10,
            "imagen": "ruta/imagen.png"
        }
        crear_item(**nuevo_item)

        items_disponibles = obtener_items_disponibles()
        self.assertEqual(len(items_disponibles), 1)

    def test_2_crear_items(self):
        # Verificar que la tabla 'items' solo contenga el item insertado en test_1
        items_disponibles = obtener_items_disponibles()
        self.assertEqual(len(items_disponibles), 1)

        nuevos_items = [
            {
                "nombre": "Nuevo Item 2",
                "talla": "M",
                "color": "Rojo",
                "precio": 19.99,
                "cantidad": 10,
                "imagen": "ruta/imagen2.png"
            },
            {
                "nombre": "Nuevo Item 3",
                "talla": "L",
                "color": "Azul",
                "precio": 29.99,
                "cantidad": 5,
                "imagen": "ruta/imagen3.png"
            },
            {
                "nombre": "Nuevo Item 4",
                "talla": "S",
                "color": "Verde",
                "precio": 14.99,
                "cantidad": 8,
                "imagen": "ruta/imagen4.png"
            },
            {
                "nombre": "Nuevo Item 5",
                "talla": "XL",
                "color": "Negro",
                "precio": 39.99,
                "cantidad": 3,
                "imagen": "ruta/imagen5.png"
            }
        ]

        for item in nuevos_items:
            crear_item(**item)

        items_disponibles = obtener_items_disponibles()
        self.assertEqual(len(items_disponibles), 5)

    def test_3_modificar_item(self):
        codigo_modificar = 2  # Código del item a modificar
        item_modificado = {
            "nombre": "Item 2 Modificado",
            "talla": "L",
            "color": "Azul",
            "precio": 24.99,
            "cantidad": 5,
            "imagen": "ruta/imagen_modificada.png"
        }
        modificar_item(codigo_modificar, **item_modificado)

        item_por_codigo = obtener_item_por_codigo(codigo_modificar)
        self.assertEqual(item_por_codigo["nombre"], "Item 2 Modificado")

    def test_4_obtener_items_disponibles(self):
        items_disponibles = obtener_items_disponibles()
        self.assertEqual(len(items_disponibles), 5)

    def test_5_obtener_item_por_codigo(self):
        codigo_item = 3  # Código del item a buscar
        item_por_codigo = obtener_item_por_codigo(codigo_item)
        self.assertEqual(item_por_codigo["codigo"], 3)

    def test_6_eliminar_item(self):
        codigo_eliminar = 4  # Código del item a eliminar
        eliminar_item(codigo_eliminar)

        item_por_codigo = obtener_item_por_codigo(codigo_eliminar)
        self.assertIsNone(item_por_codigo)
        items_disponibles = obtener_items_disponibles()
        self.assertEqual(len(items_disponibles), 4)


if __name__ == '__main__':
    unittest.main()
