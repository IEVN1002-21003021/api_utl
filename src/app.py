from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
con = MySQL(app)

@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * from alumnos order by nombre ASC'
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

def leer_alumno_bd(matricula):
  try:
    cursor=con.connection.cursor()
    sql='select * from alumnos where matricula=(0)'.format(matricula)
    cursor.execute(sql)
    datos=cursor.fetchone()
    if datos!=None:
       alumno={'matricula':datos[0], 'nombre':datos[1], 'apaterno':datos[2], 'amaterno':datos[3], 'corrreo':datos[4]}

    pass
  except Exception as ex:
    return jsonify({})
  
@app.route('/alumnos/<mat>', methods=['GET'])
def leer_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            return jsonify({'alumno': alumno, 'mensaje': "Alumno encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route("/alumnos", methods=['POST'])
def registrar_alumnos():
    try:
        alumno=leer_alumno_bd(request.json['matricula'])
        if alumno!=None:
            return jsonify({'mensaje':'Aluno ya existe','exito':False})
        else:

            cursor = con.connection.cursor()
            sql=''' INSERT INTO alumnnos (matricula, nombre, apaterno, amaterno,  correo) 
                values ('{0}','{1}','{2}','{3}','{4}')  '''.format(request.json['matricula'],request.json['nombre'],request.json['apaterno'],request.json['amaterno'],request.json['correo']) ##los tress apostrofes sirven para texto de varias lineas 
        cursor.execute(sql)
        con.connection.commit()
        # Mover el return fuera del for para que no termine en la primera iteración
        return jsonify({'message':'Alumno Agregado', 'exito': True})

    except Exception as ex:
         return jsonify({'message': "Error al conectarse a la base de datos {}". 
                        format(ex), 'exito':False})


@app.route('/alumnos/<mat>', methods=['PUT']) ##el metodod con el que se hace es put cuando quieres modificar 
def actualizar_curso(mat):
    #if (validar_matricula(mat) and validar_nombre(request.json['nombre']) and validar_apaterno(request.json['apaterno'])):
        try:
            alumno = leer_alumno_bd(mat)
            if alumno != None:
                cursor = con.connection.cursor()
                sql = """UPDATE alumnos SET nombre = '{0}', apaterno = '{1}', amaterno='{2}', correo='{3}'
                WHERE matricula = {4}""".format(request.json['nombre'], request.json['apaterno'], request.json['amaterno'],request.json['correo'], mat)
                cursor.execute(sql)
                con.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error {0} ".format(ex), 'exito': False})
        
@app.route('/alumnos/<mat>', methods=['DELETE'])
def eliminar_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = con.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = {0}".format(mat)
            cursor.execute(sql)
            con.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Alumno eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
 
      



@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1>La página que estás buscando no existe</h1>", 404  # Corregida la etiqueta

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(host='0.0.0.0', port=5000)