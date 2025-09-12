from flask import Flask, jsonify, request 
import mysql.connector
from flask_cors import CORS  
from flask import Response


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
    
########PERSONAS########

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

# Inhabilitar Persona
@app.route('/personas/<int:id>/inhabilitar', methods=['PUT'])
def inhabilitar_persona(id_persona):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        query = "UPDATE Persona SET activo = 0 WHERE id = %s"
        cursor.execute(query, (id_persona,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": f"✅ Persona con ID {id} inhabilitada correctamente."})
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
    
    
######## EMPRESAS ########

# Insertar Empresa
@app.route('/empresas', methods=['POST'])
def insertar_empresa():
    try:
        data = request.json
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        query = """
        INSERT INTO Empresa (
            nit, razon_social, nombre_usuario_url, direccion, telefono, correo_electronico,
            link_logo, link_ubicacion_maps, link_qr,
            pantone1, pantone2
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            data['nit'],
            data['razon_social'],
            data['nombre_usuario_url'],  # slug
            data['direccion'],
            data['telefono'],
            data['correo_electronico'],   # 👈 agregado
            data['link_logo'],
            data['link_ubicacion_maps'],
            data['link_qr'],
            data['pantone1'],
            data['pantone2']
        )


        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "✅ Empresa insertada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})


# Obtener todas las Empresas
@app.route('/empresas', methods=['GET'])
def obtener_empresas():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Empresa")
        empresas = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(empresas)
    except Exception as e:
        return jsonify({"error": str(e)})


# Obtener Empresa por nombre_usuario_url (slug)
@app.route('/empresas/slug/<string:nombre_usuario_url>', methods=['GET'])
def obtener_empresa_por_slug(nombre_usuario_url):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            nit, razon_social, nombre_usuario_url, direccion, telefono, correo_electronico,
            link_logo, link_ubicacion_maps, link_qr,
            pantone1, pantone2
        FROM Empresa
        WHERE nombre_usuario_url = %s
        """

        cursor.execute(query, (nombre_usuario_url,))
        empresa = cursor.fetchone()

        cursor.close()
        conn.close()

        if empresa:
            return jsonify(empresa)
        else:
            return jsonify({"error": "Empresa no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})


# Actualizar Empresa
@app.route('/empresas/<int:id_empresa>', methods=['PUT'])
def actualizar_empresa(id_empresa):
    try:
        data = request.json
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        query = """
        UPDATE Empresa SET
            nit=%s, razon_social=%s, nombre_usuario_url=%s, direccion=%s, telefono=%s, correo_electronico=%s,
            link_logo=%s, link_ubicacion_maps=%s, link_qr=%s,
            pantone1=%s, pantone2=%s
        WHERE id_empresa=%s
        """
        valores = (
            data['nit'],
            data['razon_social'],
            data['nombre_usuario_url'],
            data['direccion'],
            data['telefono'],
            data['correo_electronico'],   # 👈 agregado
            data['link_logo'],
            data['link_ubicacion_maps'],
            data['link_qr'],
            data['pantone1'],
            data['pantone2'],
            id_empresa
)


        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "✅ Empresa actualizada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})


# Inhabilitar Empresa
@app.route('/empresas/<int:id_empresa>/inhabilitar', methods=['PUT'])
def inhabilitar_empresa(id_empresa):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        query = "UPDATE Empresa SET activo = 0 WHERE id_empresa = %s"
        cursor.execute(query, (id_empresa,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": f"✅ Empresa con ID {id_empresa} inhabilitada correctamente."})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    # Endpoint para obtener Empresa y Persona desde un slug unificado
@app.route('/personas/<string:slug_unificado>', methods=['GET'])
def obtener_perfil(slug_unificado):
    try:
        # Dividir el slug: la primera parte es Empresa, el resto es Persona
        partes = slug_unificado.split('-', 1)
        if len(partes) != 2:
            return jsonify({"error": "Slug inválido. Formato esperado: empresa-persona"}), 400

        slug_empresa, slug_persona = partes[0], partes[1]

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        # Consultar Empresa
        query_empresa = """
            SELECT
                id_empresa,
                nit,
                razon_social,
                nombre_usuario_url,
                direccion,
                telefono,
                correo_electronico,  
                link_logo,
                link_ubicacion_maps,
                link_qr,
                pantone1,
                pantone2
            FROM Empresa
            WHERE nombre_usuario_url = %s
            LIMIT 1
        """

        cursor.execute(query_empresa, (slug_empresa,))
        empresa = cursor.fetchone()

        # Consultar Persona
        query_persona = """
            SELECT 
                id_persona,
                nombre,
                cargo,
                celular,
                correo_electronico,
                link_whatsapp,
                link_foto,
                nombre_usuario_url
            FROM Persona
            WHERE nombre_usuario_url = %s
            LIMIT 1
        """
        cursor.execute(query_persona, (slug_persona,))
        persona = cursor.fetchone()

        cursor.close()
        conn.close()

        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404
        if not persona:
            return jsonify({"error": "Persona no encontrada"}), 404

        return jsonify({
            "empresa": empresa,
            "persona": persona
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/contacto/<string:slug_unificado>.vcf', methods=['GET'])
def generar_vcf(slug_unificado):
    try:
        partes = slug_unificado.split('-', 1)
        if len(partes) != 2:
            return jsonify({"error": "Slug inválido. Formato esperado: empresa-persona"}), 400

        slug_empresa, slug_persona = partes[0], partes[1]

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        # Consultar Empresa
        query_empresa = """
            SELECT
                id_empresa,
                razon_social,
                direccion,
                telefono,
                correo_electronico,
                link_logo,
                link_ubicacion_maps
            FROM Empresa
            WHERE nombre_usuario_url = %s
            LIMIT 1
        """
        cursor.execute(query_empresa, (slug_empresa,))
        empresa = cursor.fetchone()

        # Consultar Persona
        query_persona = """
            SELECT 
                id_persona,
                nombre,
                cargo,
                celular,
                correo_electronico,
                nombre_usuario_url
            FROM Persona
            WHERE nombre_usuario_url = %s
            LIMIT 1
        """
        cursor.execute(query_persona, (slug_persona,))
        persona = cursor.fetchone()

        cursor.close()
        conn.close()

        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404
        if not persona:
            return jsonify({"error": "Persona no encontrada"}), 404

        # Construcción del VCF
        vcf = f"""BEGIN:VCARD
        VERSION:3.0
        N:;{persona['nombre']};;;
        FN:{persona['nombre']}
        ORG:{empresa['razon_social']}
        TITLE:{persona['cargo']}
        TEL;TYPE=CELL:{persona['celular']}
        EMAIL;TYPE=WORK:{persona['correo_electronico']}
        ADR;TYPE=WORK:;;{empresa['direccion']}
        URL:{empresa['link_ubicacion_maps'] if empresa['link_ubicacion_maps'] else ""}
        END:VCARD
        """

        response = Response(vcf)
        response.headers["Content-Type"] = "text/vcard; charset=utf-8"
        response.headers["Content-Disposition"] = f'attachment; filename="{persona["nombre"]}.vcf"'
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

########SESIONES########
    
#OBTENER SESIONES
@app.route("/sesiones/<int:empresa_id>", methods=["GET"])
def obtener_sesiones(empresa_id):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT numero_sesion, titulo, descripcion FROM Sesiones WHERE empresa_id = %s ORDER BY numero_sesion"
        cursor.execute(query, (empresa_id,))
        sesiones = cursor.fetchall()

        return jsonify(sesiones), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
            
########PRODUCTOS########            

#OBTENER PRODUCTOS
@app.route("/productos/<int:empresa_id>", methods=["GET"])
def obtener_productos(empresa_id):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                numero_producto, 
                titulo, 
                descripcion1, 
                link_producto, 
                descripcion2, 
                link_imagen_producto
            FROM Productos 
            WHERE empresa_id = %s 
            ORDER BY numero_producto
        """
        cursor.execute(query, (empresa_id,))
        productos = cursor.fetchall()

        return jsonify(productos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



########PRUEBA DE CONEXION########
    
    
@app.route('/prueba', methods=['GET'])
def ping():
    return jsonify({"message": "✅ Backend conectado con React"})
    


if __name__ == '__main__':
    app.run(debug=True)
