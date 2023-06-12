import unittest
import json
from flask import Flask

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_items(self):
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        items = json.loads(response.data)
        self.assertIsInstance(items, list)

    def test_get_item(self):
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 200)
        item = json.loads(response.data)
        self.assertIsInstance(item, dict)

    def test_get_nonexistent_item(self):
        response = self.app.get('/items/100')
        self.assertEqual(response.status_code, 404)
        message = json.loads(response.data)
        self.assertEqual(message['mensaje'], 'Item no encontrado')

    def test_create_item(self):
        data = {
            "nombre": "Nuevo Item",
            "talla": "M",
            "color": "Rojo",
            "precio": 19.99,
            "cantidad": 10,
            "imagen": "ruta/imagen.png"
        }
        response = self.app.post('/items', json=data)
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)
        self.assertEqual(message['mensaje'], 'Item creado exitosamente')

    def test_update_item(self):
        data = {
            "nombre": "Nuevo Nombre del Item",
            "talla": "L",
            "color": "Azul",
            "precio": 29.99,
            "cantidad": 5,
            "imagen": "ruta/nueva_imagen.png"
        }
        response = self.app.put('/items/1', json=data)
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)
        self.assertEqual(message['mensaje'], 'Item modificado exitosamente')

    def test_delete_item(self):
        response = self.app.delete('/items/1')
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.data)
        self.assertEqual(message['mensaje'], 'Item eliminado exitosamente')


if __name__ == '__main__':
    unittest.main()
