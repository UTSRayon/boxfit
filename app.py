from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def getIndex():  # put application's code here
    return render_template("esqueleto.html")



if __name__ == '__main__':
    app.run(debug=True)
