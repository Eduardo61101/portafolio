from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
# Permitimos que tu index.html se comunique con Python sin bloqueos de seguridad
CORS(app)

# Archivos de texto locales para guardar los datos de forma permanente
VISITAS_FILE = "total_visitas.txt"
LIKES_FILE = "total_likes.json"

# --- FUNCIONES AUXILIARES PARA LEER Y GUARDAR ---
def leer_visitas():
    if not os.path.exists(VISITAS_FILE):
        return 0
    with open(VISITAS_FILE, "r") as f:
        try:
            return int(f.read().strip())
        except:
            return 0

def guardar_visitas(cantidad):
    with open(VISITAS_FILE, "w") as f:
        f.write(str(cantidad))

def leer_likes():
    import json
    if not os.path.exists(LIKES_FILE):
        return {}
    with open(LIKES_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def guardar_likes(datos):
    import json
    with open(LIKES_FILE, "w") as f:
        json.dump(datos, f)

# --- RUTAS DEL SERVIDOR (ENDPOINTS) ---

# 1. Ruta para registrar una visita y obtener los datos actuales
@app.route("/api/visita", methods=["POST"])
def registrar_visita():
    visitas_actuales = leer_visitas()
    visitas_actuales += 1
    guardar_visitas(visitas_actuales)
    
    likes_actuales = leer_likes()
    
    return jsonify({
        "visitas": visitas_actuales,
        "likes": likes_actuales
    })

# 2. Ruta para procesar un "Me Gusta" individual de los renders
@app.route("/api/like", methods=["POST"])
def procesar_like():
    data = request.json
    id_imagen = data.get("id_imagen")
    
    likes_totales = leer_likes()
    if id_imagen:
        likes_totales[id_imagen] = likes_totales.get(id_imagen, 0) + 1
        guardar_likes(likes_totales)
        
    return jsonify({
        "status": "success",
        "likes_actuales": likes_totales.get(id_imagen, 0)
    })

# Arrancamos el servidor local en el puerto 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)