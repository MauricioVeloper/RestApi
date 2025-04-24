from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de avisos y notas en memoria
avisos = [
    {"id": 1, "mensaje": "Reunión a las 10 AM"},
    {"id": 2, "mensaje": "Entrega del reporte el viernes"}
]

@app.route('/avisos', methods=['GET'])
def obtener_avisos():
    return jsonify(avisos)

@app.route('/avisos', methods=['POST'])
def agregar_aviso():
    nuevo_aviso = request.get_json()
    nuevo_aviso["id"] = len(avisos) + 1
    avisos.append(nuevo_aviso)
    return jsonify(nuevo_aviso), 201

@app.route('/avisos/<int:aviso_id>', methods=['PUT'])
def actualizar_aviso(aviso_id):
    datos = request.get_json()
    for aviso in avisos:
        if aviso["id"] == aviso_id:
            aviso["mensaje"] = datos.get("mensaje", aviso["mensaje"])
            return jsonify(aviso)
    return jsonify({"error": "Aviso no encontrado"}), 404

@app.route('/avisos/<int:aviso_id>', methods=['DELETE'])
def eliminar_aviso(aviso_id):
    global avisos
    avisos = [aviso for aviso in avisos if aviso["id"] != aviso_id]
    return jsonify({"mensaje": "Aviso eliminado"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

