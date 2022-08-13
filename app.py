import urllib.request

from flask import Flask,render_template,request,make_response,redirect,url_for
import pyrebase
from pyrebase.pyrebase import storage
import os
import json
#from models.usuario import usuario
from models.usuario import Usuario
from utils.Fecha import Fecha
from models.Usuario_Colegiatura import  Usuario_Colegiatura
from models.PagosReporte import PagosReporte
from models.Pagos import Pagos
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import base64
from flask_qrcode import QRcode

from firebase import Firebase





#variable de configuracion
config={
  "apiKey": "AIzaSyBTY_jIHQE5Khyq0__BNhxylrApmYqSMZM",
  "authDomain": "boxfit-d57c1.firebaseapp.com",
  "databaseURL": "https://boxfit-d57c1-default-rtdb.firebaseio.com",
  "storageBucket": "boxfit-d57c1.appspot.com",
  "projectId": "boxfit-d57c1",
  #"messagingSenderId": "730838439699",
  #"appId": "1:730838439699:web:bce749eb12d63a7ee3ace6",
  #"serviceAccount": "serviceAccountKey.json"


}

firebase=pyrebase.initialize_app(config)
db=firebase.database()
storage=firebase.storage()

fire=Firebase(config)


#para consultas con condición
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote




app = Flask(__name__)
QRcode(app)


@app.route("/",methods=["GET"])
def principal():
    historial_de_pagos=[]
    cantidad_usuarios=0
    cantidad_asistencia_usuarios=0
    try:
        datos_persona = db.child("clientes").get().val()
        cantidad_usuarios = len(list(datos_persona.values()))
        #print("Personas ",list(datos_persona.keys()))
        for llave in list(datos_persona.keys()):
           # print("llave",llave)
            datos_persona = db.child("clientes").child(str(llave)).get().val()
            datos_persona = list(datos_persona.values())
            actividad_persona = list(datos_persona[0].values())

            try:
                lista_pagos = db.child("pagos").child(llave).get().val()
                lista_pagos = list(lista_pagos.values())

                fecha_ingreso = actividad_persona[1].split(" ")[0]

                historial_pagos = Fecha().calcularPagos(fecha_ingreso, lista_pagos, float(actividad_persona[4]))
                historial_de_pagos.append(historial_pagos)
                #print("Historial pagos: ", historial_pagos)
            except:
                fecha_ingreso = actividad_persona[1].split(" ")[0]
                lista_ = [{"fecha": fecha_ingreso, "importe": -float(actividad_persona[4]),
                           "observaciones": "Primer pago de colegiatura"}]

                historial_pagos = Fecha().calcularPagos(fecha_ingreso, lista_, float(actividad_persona[4]))
                historial_de_pagos.append(historial_pagos)
                print("error no hay datos")



    except:
        print("error")


        #  lista = db.child("clientes").order_by_child("correo").equal_to(correo).limit_to_first(1).get().val()

    #obtener las asistencias de los usuarios por dia
    try:
        datos_asistencia = db.child("asistencia").order_by_child("fecha").equal_to(Fecha.obtenerFechaSinHora()).get().val()
        cantidad_asistencia_usuarios=len(list(datos_asistencia.values()))
        #print("cantidad de asistencia ",cantidad_asistencia_usuarios)
    except:
        print("Error 2")



    #print("Lista de pagos",historial_de_pagos[1])
    #print("Lista de pagos3",list(historial_de_pagos))
    saldos_estatus=Fecha.calcularSaldosPendientesFavor(list(historial_de_pagos))
    print("asi estamos",saldos_estatus)
    return render_template("principal.html",cantidad_usuarios=cantidad_usuarios,cantidad_asistencia_usuarios=cantidad_asistencia_usuarios,fecha=Fecha.obtenerFechaSinHora(),saldos_estatus=saldos_estatus)


@app.route("/leer",methods=["GET"])
def leerQR():
    return render_template("lecturaasistencia.html")

#reporte de asistencia
@app.route("/reporteasistencia",methods=["GET","POST"])
def reporteasistencia():
    if request.method == "POST":
        fechainicial = request.form.get('fechainicial')
        fechafinal = request.form.get('fechafinal')
        reporte_asistencia=db.child("asistencia").order_by_child("fecha").start_at(fechainicial).end_at(fechafinal+ "23:59:59").get().val()
        #obtener imagen del servidor
        lista_ruta_imagen=[]
        for k in reporte_asistencia.values():
            storage = fire.storage()
            codigo=k["ruta"]
            ruta_url = storage.child(f"perfil/{codigo}.jpg").get_url(None)
            lista_ruta_imagen.append(ruta_url)

        return render_template("reporteasistencia.html",resultado=reporte_asistencia.values(),lista_ruta_image=lista_ruta_imagen)
    elif request.method=="GET":
        return render_template("reporteasistencia.html")
    else:
        print("error ")

#reporte de pagos
@app.route("/reporte",methods=["GET","POST"])
def reporte():
    if request.method == "POST":
        #obtener nombre y datos de las personas
        lista_clientes=db.child("clientes").get().val()
        arreglo_personas_pagos=[]
        fechainicial = request.form.get('fechainicial')
        fechafinal = request.form.get('fechafinal')
        for i in lista_clientes.items():
            #print(i[1]["nombre"]) obtiene nombre de las perosnas
            #print(i[0]) obtienne los key de los nodos raiz
           # print("----",i[1]["nombre"])

            #persona_nueva.asignar_datos_basicos(i[1]["nombre"],i[1]["apellido"],i[1]["telefono"],i[0])



            try:
                print("Inicial: ",fechainicial)
                print("Final: ",fechafinal)
                resultados = db.child("pagos").child(i[0]).order_by_child("fecha").start_at(fechainicial).end_at(fechafinal+ "23:59:59").get().val().values()

                l=list(resultados)
                for y in l:
                    #(self, importe, observaciones, fecha):
                    #persona_nueva_pagos.asignar_datos_pagos()
                    #print(y["importe"])
                    print("con")
                    persona_nueva_pagos = PagosReporte()
                    persona_nueva_pagos.asignar_datos_pagos(y["importe"],y["observaciones"],y["fecha"],i[1]["nombre"],i[1]["apellido"],i[1]["telefono"],i[0])
                    arreglo_personas_pagos.append(persona_nueva_pagos)

            except  Exception as exception:
                    print("Exception: {}".format(type(exception).__name__))
                    print("Exception message: {}".format(exception))



        return render_template("reportepagos.html",lista_de_pagos=arreglo_personas_pagos)
    elif request.method=="GET":
        print("soy get")
        return render_template("reportepagos.html")
    else:
        print("Error al consultar datos")

@app.route("/informacion/")
def informacion():

    try:
        qr = request.args.get("qr")
        print("QR persona ",qr)
        datos_persona = db.child("clientes").child(str(qr)).get().val()
        datos_completos = list(datos_persona.values())
        nombre=datos_completos[4]
        apellidos=datos_completos[1]
        telefono=datos_completos[5]

        data={"nombre":nombre+" "+apellidos,"telefono":telefono,"fecha":Fecha.obtenerFechaSinHora(),"hora":Fecha.obtenerSoloHora(),"ruta":qr}

        #db.child("asistencia").child(Fecha.obtenerFechaSinHora()).child(str(qr)).push(data)
        db.child("asistencia").push(data)
        return redirect(url_for('leerQR', estado=1))
    except:
        print("errrt")
        return redirect(url_for('leerQR', estado=2))





@app.route('/registroPagos',methods=["POST"])
def registroPagos():
    if request.method=="POST":
        codigo=request.form.get('codigo')
        importe=request.form.get('importe')
        observaciones=request.form.get('observaciones')
        fecha=Fecha.obtenerFechaSinHora()
        data={"importe":importe,"observaciones":observaciones,"fecha":Fecha.obtenerFechaConHora()}
        db.child("pagos").child(str(codigo)).push(data)
        return redirect(url_for('historial',codigo=codigo))


@app.route('/historial/<codigo>',methods=["GET"])
def historial(codigo):
    datos_persona = db.child("clientes").child(str(codigo)).get().val()

    datos_persona=list(datos_persona.values())
    actividad_persona=list(datos_persona[0].values())

    try:
        storage=fire.storage()
        ruta_url=storage.child(f"perfil/{codigo}.jpg").get_url(None)
       # print("ruta url: ",ruta_url)

    except ValueError:
        print ("Ocurrio un error")

    #consulta de pagos
    try:
        lista_pagos=db.child("pagos").child(codigo).get().val()
        lista_pagos=list(lista_pagos.values())


        #print("Actividad persona: ",actividad_persona[1])
        fecha_ingreso=actividad_persona[1].split(" ")[0]
        #print("tengo datos en abono",lista_pagos)
        historial_pagos=Fecha().calcularPagos(fecha_ingreso,lista_pagos,float(actividad_persona[4]))
        print("Historial pagos: ",historial_pagos)

        return render_template("historial.html", datos_persona=datos_persona, actividad_persona=actividad_persona,
                               ruta_url=ruta_url, codigo_persona=codigo, lista_pagos=lista_pagos,historial_pagos=historial_pagos)
    except:
        print("Error sin datos ")

        fecha_ingreso = actividad_persona[1].split(" ")[0]
        lista_ = [{"fecha": fecha_ingreso, "importe": -float(actividad_persona[4]), "observaciones": "Primer pago de colegiatura"}]


        historial_pagos=Fecha().calcularPagos(fecha_ingreso,lista_,float(actividad_persona[4]))

        return render_template("historial.html", datos_persona=datos_persona, actividad_persona=actividad_persona,
                               ruta_url=ruta_url, codigo_persona=codigo,historial_pagos=historial_pagos)


@app.route("/listaclientes")
def listaclientes():
    datos_completos = db.child("clientes").get().val()
    indices=datos_completos
    datos_completos = list(datos_completos.values())
    #lista = list(datos_completos[0].values())
    #print("datos completo: ",lista[0]["actividad"])
    lista_completa=[]
    contador=0
    contador2=0
    indices=list(indices.keys())
    #print("Lista usuarios: ",indices[1])
    #lista de usuarios completa
    lista_usuarios_completa=[]
    for x in datos_completos:
        lista_actividades=[]
        lista_informacion=[]

        for y in list(datos_completos[contador2].values()):
            if contador==0:
                lista_nueva=list(y.values())
                #print("nueva lista",lista_nueva)
                for k in lista_nueva:
                 #   print("res: ",k)
                    lista_actividades.append(k)
            else:
                #print("---<",y)
                lista_informacion.append(y)
                #print("contador:",contador)


            contador=contador+1
      #  print("Lista Información: ", lista_informacion)
       # print("Lista actividades: ", lista_actividades)
        usuario = Usuario()
        usuario.apellido = lista_informacion[0]
        usuario.correo = lista_informacion[1]
        usuario.direccion = lista_informacion[2]
        usuario.nombre = lista_informacion[3]
        usuario.telefono = lista_informacion[4]
        usuario.actividad = lista_actividades[0]
        usuario.fecha_inicio = lista_actividades[1]
        usuario.horario = lista_actividades[2]
        usuario.inscripcion = lista_actividades[3]
        usuario.precio = lista_actividades[4]
        usuario.codigo=indices[contador2]

        lista_usuarios_completa.append(usuario)

        contador=0
        contador2=contador2+1
    contador2=0





    return render_template("listado_clientes.html",lista_usuarios_completa=lista_usuarios_completa)

@app.route('/altapersona')
def altapersona():  # put application's code here
    lista=db.child("clientes").get()

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

        #neew_clien=Usuario(nombre,apellido,direccion,telefono,correo)
        neew_clien = Usuario()
        neew_clien.asignarDatos(nombre,apellido,direccion,telefono,correo)
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
      #  print("datos completo: ",datos_completos)
       # print("lista ",lista)



        #generar Imagen QR con base al codigo del usuario



        return render_template("registro3.html",persona_datos=datos_completos,persona_actividades=lista,codigoqr=codigo,imagen_perfil=imagen_perfil)
    else:
        return render_template("registro.html")






@app.route('/table')
def table():  # put application's code here
    return render_template("tabla.html")




if __name__ == '__main__':
    app.run(debug=True)
