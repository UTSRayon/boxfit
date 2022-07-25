import os.path

from flask import Flask,render_template,request,make_response
import pyrebase
from flask import url_for
import json
from models.usuario import usuario
from utils.Fecha import Fecha
from models.Usuario_Colegiatura import  Usuario_Colegiatura
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import base64
from flask_qrcode import QRcode
import pdfkit
from glob import glob



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
storage=firebase.storage()




#para consultas con condición
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote




app = Flask(__name__)
QRcode(app)


@app.route('/prueba')
def prueba():
    lista_clientes=db.child("clientes").get().val()

    return render_template("tabla.html",elementos_clientes=lista_clientes.values())


@app.route("/listaclientes")
def listaclientes():
    return render_template("listado_clientes.html")

@app.route('/')
def getIndex():  # put application's code here
    lista=db.child("clientes").get()
    """try:
        lista_clientes=lista.val()
        lista_wars=lista_clientes.keys()
        lista_war_final=list(lista_wars)
        print("lista clientes: ",lista_clientes)
        print("lista clientes: ",lista_wars)
        print("lista clientes: ",lista_war_final)
        return render_template("registro.html",lista_cliente=lista_clientes.values(),lista_war_final=lista_war_final)
    except:
        print("error no hay nada")"""
    #retornamos el forumulario registro
    return render_template("registro.html")

#ruta para mostrar formulario de registro
@app.route('/add')
def add():
    return render_template("registro.html")


app.config['UPLOAD_FOLDER'] = './static'
#guardatos de formulario en fb
@app.route('/save_data',methods=['POST'])
def save_data():

    if request.method=="POST":
        f=request.files['foto']
        nombre=request.form.get('nombre')
        apellido=request.form.get('apellido')
        direccion=request.form.get('direccion')
        telefono=request.form.get('telefono')
        correo=request.form.get('correo')

        neew_clien=usuario(nombre,apellido,direccion,telefono,correo)
        submit_form =json.dumps(neew_clien.__dict__)

        moon = json.loads(submit_form)
        db.child("clientes").push(moon)

        lista = db.child("clientes").order_by_child("correo").equal_to(correo).limit_to_first(1).get().val()
        #print(lista)
        x=list(lista.values())
        #para obtener codigo de cliente
        codigo_cliente=str(list(lista.keys()))[1:-1]
        codigo_cliente=codigo_cliente.replace("'","")

        #subir la foto a FireStore
        storage.child(f"perfil/{codigo_cliente}.jpg").put(f)

        #obtener precio de las actividades
        precios=db.child("colegiaturas").get().val()
        lista_precios=list(precios.values())
        #obtener precio inscripcion
        inscripcion=db.child("inscripcion").get().val()
        inscripcion=inscripcion.values()
        inscripcion=list(inscripcion)






        """img = Image.open(f.stream)
        with BytesIO() as buf:
            img.save(buf, 'jpeg')
            image_bytes = buf.getvalue()
        encoded_string = base64.b64encode(image_bytes).decode()"""

        return render_template("registro2.html",lista=x,imagen_perfil=convertir_imagen(f),codigo_cliente=codigo_cliente,lista_precios=lista_precios,inscripcion=inscripcion[0]),200


def convertir_imagen(imagen):
    img = Image.open(imagen.stream)
    with BytesIO() as buf:
        img.save(buf, 'jpeg')
        image_bytes = buf.getvalue()
    encoded_string = base64.b64encode(image_bytes).decode()
    return encoded_string



@app.route('/re',methods=['POST'])
def re():  # put application's code here
    return render_template("registro2.html")

@app.route('/registro2',methods=["POST"])
def registro2():  # put application's code here
    if request.method=="POST":
        #recibir variables
        codigo=request.form.get("codigo")
        inscripcion=request.form.get("inscripcion")
        colegiatura=request.form.get("colegiatura")
        horario=request.form.get("horario")
        inscripcion=inscripcion.replace("$","")
        imagen_perfil=request.form.get("perfil")

        #dividir colegiatura por /
        datos=colegiatura.split("/")
        costo=datos[1].replace("$","")


        #generar un registro a la base de datos
        try:
            sub_nodo=Usuario_Colegiatura(inscripcion,datos[0],costo,horario,Fecha.obtenerFechaConHora())
            objeto_enviar=json.dumps(sub_nodo.__dict__)
            objeto_enviar=json.loads(objeto_enviar)
            db.child("clientes").child(str(codigo)).push(objeto_enviar)
        except:
            print("Error al subir el archivo")

        datos_completos= db.child("clientes").child(str(codigo)).get().val()
        datos_completos=list(datos_completos.values())
        lista=list(datos_completos[0].values())



        #generar Imagen QR con base al codigo del usuario



        return render_template("registro3.html",persona_datos=datos_completos,persona_actividades=lista,codigoqr=codigo,imagen_perfil=imagen_perfil)
    else:
        return render_template("registro.html")






@app.route('/table')
def table():  # put application's code here
    return render_template("tabla.html")




if __name__ == '__main__':
    app.run(debug=True)
