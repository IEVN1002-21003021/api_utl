from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
con = MySQL(app)

@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM alumnos'
        cursor.execute(sql)
        datos = cursor.fetchall()

        alumnos = []
        for fila in datos:
            alumno = {
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]  # Corregido el error tipográfico
            }
            alumnos.append(alumno)
        
        # Mover el return fuera del for para que no termine en la primera iteración
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de Alumnos', 'exito': True})

    except Exception as ex:
        # Proporcionar más detalles sobre el error
        return jsonify({
            "mensaje": f"Error al conectar a la base de datos: {str(ex)}",
            'exito': False
        })

    finally:
        # Cerrar el cursor para liberar recursos
        cursor.close()

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1>La página que estás buscando no existe</h1>", 404  # Corregida la etiqueta

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(host='0.0.0.0', port=5000)