from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

# Definir la app Flask

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

#CONFIGURAR EL QSlALCHEMY CON ORACLE CLOUD
db = SQLAlchemy(app)

#DEFINIR EL MODELO DE LA BASE DE DATOS

class Fichas(db.Model):
    __tablename__ = 'FICHAS'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(200), nullable=False)

    # Campos para tipo libro
    nombre_autor = db.Column(db.String(200), nullable=True)
    apellido_autor = db.Column(db.String(200), nullable=True)
    pagina = db.Column(db.Integer, nullable=True)

    # Campos para tipo video
    nombre = db.Column(db.String(200), nullable=True)
    tema = db.Column(db.String(200), nullable=True)
    link = db.Column(db.String(200), nullable=True)

    # Común a ambos
    anio = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nombre_autor": self.nombre_autor,
            "apellido_autor": self.apellido_autor,
            "pagina": self.pagina,
            "nombre": self.nombre,
            "tema": self.tema,
            "anio": self.anio,
            "link": self.link
        }

# RUTA PARA OBTENER TODOS LOS PRODUCTOS
@app.route('/FICHAS', methods=['POST'])
@app.route('/api/fichas', methods=['POST'])
def crear_ficha():
    data = request.get_json()
    tipo = data.get('tipo')

    if tipo == 'libro':
        required = ['nombre_autor', 'apellido_autor', 'anio', 'pagina']
    elif tipo == 'video':
        required = ['nombre', 'tema', 'anio', 'link']
    else:
        return jsonify({'error': 'Tipo inválido'}), 400

    for campo in required:
        if not data.get(campo):
            return jsonify({'error': f'Falta el campo: {campo}'}), 400

    ficha = Fichas(**data)
    db.session.add(ficha)
    db.session.commit()
    return jsonify({'mensaje': 'Ficha creada', 'ficha': ficha.to_dict()}), 201


@app.route('/FICHAS', methods=['GET'])
@app.route('/api/fichas', methods=['GET'])
def listar_fichas():
    todas = Fichas.query.all()
    return jsonify([f.to_dict() for f in todas]), 200


@app.route('/FICHAS/<int:id>', methods=['PUT'])
@app.route('/api/fichas/<int:id>', methods=['PUT'])
def modificar_ficha(id):
    data = request.get_json()
    ficha = Fichas.query.get(id)
    if not ficha:
        return jsonify({'error': 'Ficha no encontrada'}), 404

    for key, value in data.items():
        if hasattr(ficha, key):
            setattr(ficha, key, value)

    db.session.commit()
    return jsonify({'mensaje': 'Ficha actualizada', 'ficha': ficha.to_dict()}), 200

@app.route('/FICHAS/<int:id>', methods=['DELETE'])
@app.route('/api/fichas/<int:id>', methods=['DELETE'])
def eliminar_ficha(id):
    ficha = Fichas.query.get(id)
    if not ficha:
        return jsonify({'error': 'Ficha no encontrada'}), 404

    db.session.delete(ficha)
    db.session.commit()
    return jsonify({'mensaje': 'Ficha eliminada'}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)