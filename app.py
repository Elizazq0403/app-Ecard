from flask import Flask, jsonify, request 
import mysql.connector
from flask_cors import CORS  

app = Flask(__name__)

CORS(app)

# Datos de conexión
config = {
    "host": "162.241.61.135",
    "user": "asherind_web-z",
    "password": "Web-Z2025*",
    "database": "asherind_web-z",
    "port": 3306
}

@app.route('/')
def index():
    return '✅ API Flask en funcionamiento.'

@app.route('/test-db')
def test_db_connection():
    try:
        conn = mysql.connector.connect(**config)
        conn.close()
        return jsonify({"message": "Conexion a la base de datos exitosa"})
    except Exception as e:
        return jsonify({"error": str(e)})
    

# Insertar Personas
@app.route('/personas', methods=['POST'])
def insertar_persona():
    try:
        data = request.json
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        query = """
        INSERT INTO Persona (
            nombre, celular, link_foto, cargo, correo_electronico,
            link_whatsapp, link_facebook, link_instagram, link_pagina_web, nombre_usuario_url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            data['nombre'],
            data['celular'],
            data['link_foto'],
            data['cargo'],
            data['correo_electronico'],
            data['link_whatsapp'],
            data['link_facebook'],
            data['link_instagram'],
            data['link_pagina_web'],
            data['nombre_usuario_url']
        )

        cursor.execute(query, valores)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Persona insertada correctamente ✅"})

    except Exception as e:
        return jsonify({"error": str(e)})

    

# Obtener Personas
@app.route('/personas', methods=['GET'])
def obtener_personas():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Persona")
        personas = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(personas)
    
    except Exception as e:
        return jsonify({"error": str(e)})

    
# Actualizar Persona
@app.route('/personas/<int:id>', methods=['PUT'])
def actualizar_persona(id):
    datos = request.get_json()

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        query = """
        UPDATE Persona SET
            nombre = %s,
            celular = %s,
            link_foto = %s,
            cargo = %s,
            correo_electronico = %s,
            link_whatsapp = %s,
            link_facebook = %s,
            link_instagram = %s,
            link_pagina_web = %s,
            nombre_usuario_url= %s
        WHERE id = %s
        """
        valores = (
            datos['nombre'],
            datos['celular'],
            datos['link_foto'],
            datos['cargo'],
            datos['correo_electronico'],
            datos['link_whatsapp'],
            datos['link_facebook'],
            datos['link_instagram'],
            datos['link_pagina_web'],
            datos['nombre_usuario_url'],
            id
        )

        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Persona actualizada correctamente ✅"})

    except Exception as e:
        return jsonify({"error": str(e)})

# Eliminar Persona    
@app.route('/personas/<int:id>', methods=['DELETE'])
def eliminar_persona(id):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Persona WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": f"✅ Persona con ID {id} eliminada correctamente."})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
# Obtener Persona por nombre_usuario_url (slug) con campos específicos
@app.route('/personas/slug/<string:nombre_usuario_url>', methods=['GET'])
def obtener_persona_por_slug(nombre_usuario_url):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                nombre,
                celular,
                link_foto,
                cargo,
                correo_electronico,
                link_whatsapp
            FROM Persona
            WHERE nombre_usuario_url = %s
        """
        cursor.execute(query, (nombre_usuario_url,))
        persona = cursor.fetchone()

        cursor.close()
        conn.close()

        if persona:
            return jsonify(persona)
        else:
            return jsonify({"error": "Persona no encontrada"}), 404

    except Exception as e:
        return jsonify({"error": str(e)})


    
    
    
@app.route('/prueba', methods=['GET'])
def ping():
    return jsonify({"message": "✅ Backend conectado con React"})
    


if __name__ == '__main__':
    app.run(debug=True)
