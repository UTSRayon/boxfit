from flask import Flask,render_template

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



if __name__ == '__main__':
    app.run(debug=True)
