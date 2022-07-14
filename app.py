from flask import Flask,render_template,request
import pyrebase
from flask import url_for
import json

from models.user2 import user2
from models.usuario import usuario
from datetime import date
from collections import OrderedDict



#variable de configuracion
config={
  "apiKey": "AIzaSyBTY_jIHQE5Khyq0__BNhxylrApmYqSMZM",
  "authDomain": "boxfit-d57c1.firebaseapp.com",
  "databaseURL": "https://boxfit-d57c1-default-rtdb.firebaseio.com",
  "projectId": "boxfit-d57c1",
  "storageBucket": "boxfit-d57c1.appspot.com",
  "messagingSenderId": "730838439699",
  "appId": "1:730838439699:web:bce749eb12d63a7ee3ace6",
}

firebase=pyrebase.initialize_app(config)
db=firebase.database()

#para consultas con condición
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote




app = Flask(__name__)

@app.route('/prueba')
def prueba():
    lista_clientes=db.child("clientes").get().val()

    return render_template("tabla.html",elementos_clientes=lista_clientes.values())

@app.route('/')
def getIndex():  # put application's code here
    lista=db.child("clientes").get()
    try:
        lista_clientes=lista.val()
        lista_wars=lista_clientes.keys()
        lista_war_final=list(lista_wars)
        return render_template("registro.html",lista_cliente=lista_clientes.values(),lista_war_final=lista_war_final)
    except:
        return render_template("registro.html")

#ruta para mostrar formulario de registro
@app.route('/add')
def add():
    return render_template("registro.html")

#guardatos de formulario en fb
@app.route('/save_data',methods=['POST'])
def save_data():
    nombre=request.form.get('nombre')
    apellido=request.form.get('apellido')
    direccion=request.form.get('direccion')
    telefono=request.form.get('telefono')
    correo=request.form.get('correo')
    neew_clien=usuario(nombre,apellido,direccion,telefono,correo)
    submit_form =json.dumps(neew_clien.__dict__)

    moon = json.loads(submit_form)
    db.child("clientes").push(moon)

    #db.child("clientes").push({"nombre": nombre, "apellido":apellido, "direccion":direccion, "telefono":telefono, "correo":correo })

    #obtener el Id, nombre, telefono
    #lista = db.child("temperatura").child(str(id)).get().val()
    #lista=db.child("clientes").child(str("-N6scfjp2o-7cm-EGwE7")).get()
    lista = db.child("clientes").order_by_child("correo").equal_to(correo).limit_to_first(1).get().val()
    #print(lista)
    #print(dict(lista))
    return render_template("registro2.html",lista_persona=lista.values())

#Registro 2 --------------------------------------------------------------------------------------------------------------------------------
@app.route('/opti')
def opti():
    return render_template("registro3html")

#capturar datos y guardarlos en fb
@app.route('/blend',methods=['POST'])
def blend():
    nombre=request.form.get('nombre')
    telefono=request.form.get('telefono')
    colegiatura= request.form.get('colegiatura')

    #fecha = request.form.get('fecha')
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")


    horario= request.form.get('horario')
    neew_clien=user2(nombre,telefono,colegiatura,d1,horario)
    submit_form = json.dumps(neew_clien.__dict__)

    moon = json.loads(submit_form)
    db.child("leones").push(moon)
    print("d1 =", d1)
    #db.child("leones").push({"nombre": nombre,  "telefono":telefono})
    return render_template("registro3.html")





@app.route('/re',methods=['POST'])
def re():  # put application's code here
    return render_template("registro2.html")

@app.route('/re2')
def re2():  # put application's code here
    return render_template("registro3.html")
@app.route('/table')
def table():  # put application's code here
    return render_template("tabla.html")



if __name__ == '__main__':
    app.run(debug=True)
