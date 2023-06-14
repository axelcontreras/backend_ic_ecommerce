from flask import Flask, jsonify, request
import json
import psycopg2
import logging

from utiles import *

app = Flask(__name__)
app.debug = True


@app.route('/items', methods=['GET'])
def get_items():
    items = obtener_items_disponibles()
    return jsonify(items)

@app.route('/items/<int:codigo>', methods=['GET'])
def get_item(codigo):    
    item = obtener_item_por_codigo(codigo)
    if item:
        return jsonify(item)
    else:
        return jsonify({'mensaje': 'Item no encontrado'}), 404

@app.route('/items', methods=['POST'])
def create_item():
    nuevo_item = request.get_json()
    print("got request", nuevo_item)  
    crear_item(**nuevo_item)
    return jsonify({'mensaje': 'Item creado exitosamente'}), 200

@app.route('/items/<int:codigo>', methods=['PUT'])
def update_item(codigo):
    item_modificado = request.get_json()
    modificar_item(codigo, **item_modificado)
    return jsonify({'mensaje': 'Item modificado exitosamente'})

@app.route('/items/<int:codigo>', methods=['DELETE'])
def delete_item(codigo):
    eliminar_item(codigo)
    return jsonify({'mensaje': 'Item eliminado exitosamente'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5131)

