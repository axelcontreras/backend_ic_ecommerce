from datetime import datetime
import os
from uuid import uuid4
from flask import Flask, jsonify, request
import json
import psycopg2
import logging
from flask_cors import CORS
from utiles import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
UPLOAD_FOLDER = 'ruta'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'pdf'}
# Configurar la ruta estática
app.static_url_path = '/static'
app.static_folder = 'ruta'


# Función para verificar la extensión del archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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

"""@app.route('/items', methods=['POST'])
def create_item():
    nuevo_item = request.get_json()
    print("got request", nuevo_item)  
    crear_item(**nuevo_item)
    return jsonify({'mensaje': 'Item creado exitosamente'}), 200
"""
@app.route('/items/<int:codigo>', methods=['PUT'])
def update_item(codigo):
    item_modificado = request.get_json()
    modificar_item(codigo, **item_modificado)
    return jsonify({'mensaje': 'Item modificado exitosamente'})

@app.route('/items/<int:codigo>', methods=['DELETE'])
def delete_item(codigo):
    eliminar_item(codigo)
    return jsonify({'mensaje': 'Item eliminado exitosamente'})

@app.route('/items', methods=['POST'])
def create_item():
    item = {         
            "imagen": os.path.join(app.config['UPLOAD_FOLDER'], "sin_imagen.png")
           }
    # Verifica si se proporcionó un archivo en la solicitud
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        
        # Verifica la extensión del archivo
        if imagen and allowed_file(imagen.filename):
            # Genera un nombre de archivo único basado en el timestamp y el UUID
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid4().hex)
            filename = f"{timestamp}_{unique_id}_{secure_filename(imagen.filename)}"
            
            # Guarda el archivo en la carpeta de carga
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Obtiene los datos del formulario
            nombre = request.form.get('nombre')
            color = request.form.get('color')
            talla = request.form.get('talla')
            precio = request.form.get('precio')
            cantidad = request.form.get('cantidad')
            if nombre is not None and talla is not None and color is not None and precio is not None and cantidad is not None:
                item['nombre'] = nombre
                item['talla'] = talla
                item['color'] = color
                item['precio'] = precio
                item['cantidad'] = cantidad
                item['imagen'] = 'static/' + filename
                crear_item(**item)
                print(item.get('imagen'))
                return jsonify({'mensaje': 'Item creado exitosamente'}), 200
            else:
                mensaje_error = 'Faltan datos obligatorios:'
                if nombre is None:
                    mensaje_error += ' nombre'
                if talla is None:
                    mensaje_error += ' talla'
                if color is None:
                    mensaje_error += ' color'
                if precio is None:
                    mensaje_error += ' precio'
                if cantidad is None:
                    mensaje_error += ' cantidad'
                return mensaje_error, 400
            
    return 'Error al cargar el archivo.', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5131)

