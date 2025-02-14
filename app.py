from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Crar instancia

app = Flask(__name__)


#Configuracion de DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://enrique:bQUyV9mgcNsNc3HFKqWhPXBAozdxcjQ7@dpg-cuiikit2ng1s73dkdhl0-a.oregon-postgres.render.com/db_cetech_kcec'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos

class Alumno(db.Model):
    __tablename__ = 'alumnos'
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

    def to_dict(self):
        return{
            'no_control': self.no_control,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'semestre': self.semestre,
        }


#Ruta raiz

@app.route('/')
def index():
    #Realiza una consulta de todos los alumnos
    alumnos = Alumno.query.all()

    return render_template('index.html', alumnos=alumnos)



#Ruta secundaria para crear un nuevo alumno

@app.route('/alumnos/new', methods= ['GET', 'POST'])
def create_alumnos():
    if request.method=='POST':
        #Aqui se va a retornar algo.
        no_control = request.form['no_control']
        nombre = request.form['nombre']
        ap_paterno = request.form['ap_paterno']
        ap_materno = request.form['ap_materno']
        semestre = request.form['semestre']

        nvo_alumno = Alumno(no_control=no_control, nombre= nombre, ap_paterno=ap_paterno, ap_materno=ap_materno, semestre=semestre)

        db.session.add(nvo_alumno)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create_alumno.html')

#Eliminar un alumno

@app.route('/alumnos/delete/<string:no_control>')
def delete_estudiante(no_control): 
    alumno = Alumno.query.get(no_control)
    if alumno:
        db.session.delete(alumno)
        db.session.commit()
    return redirect(url_for('index'))

#Editar un alumno

@app.route('/alumnos/update/<string:no_control>' , methods= ['GET', 'POST'])
def update_estudiante(no_control): 
    alumno = Alumno.query.get(no_control)
    if request.method == 'POST':
        alumno.nombre = request.form['nombre']
        alumno.ap_paterno = request.form['ap_paterno']
        alumno.ap_materno = request.form['ap_materno']
        alumno.semestre = request.form['semestre']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', alumno=alumno)

if __name__=='__main__':
    app.run(debug=True)