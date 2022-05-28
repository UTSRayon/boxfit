from flask import Flask,render_template
import pyrebase





#variable de configuracion
config={
    "apiKey": "AIzaSyDJi3FX5e5qwuy72P5RbuVMm0O5-rHyxlM",
    "authDomain": "boxfit-153ae.firebaseapp.com",
    "databaseURL": "https://boxfit-153ae-default-rtdb.firebaseio.com",
    "projectId": "boxfit-153ae",
    "storageBucket": "boxfit-153ae.appspot.com",
    "messagingSenderId": "331502980923",
    "appId": "1:331502980923:web:5b213d4742c9d041f2711e"
}

firebase=pyrebase.initialize_app(config)
db=firebase.database()


app = Flask(__name__)


@app.route('/')
def getIndex():  # put application's code here
    return render_template("registro.html")

@app.route('/re')
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
