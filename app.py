from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/usuario/registrar/", methods=["GET", "POST"])
def registrar_usuario():
    if request.method == "POST":
        print("Hiciste una peticions POST")
        password = generate_password_hash(request.form["password"])
        usuario = Usuario.query.filter_by(nombre=request.form["nombre"]).first()
        
        if usuario:
            flash("El nombre de usuario ya existe, cambielo",  category="mensaje--error")

        if check_password_hash(password, request.form["password-c"]):
            nuevoUsuario = Usuario(nombre=request.form["nombre"], password=password)

            db.session.add(nuevoUsuario)
            db.session.commit()

            flash("Te has registrado exitosamente", category="mensaje--success")

            return redirect(url_for("ingresar_usuario"))
        else:
            flash("El password no coincide intentalo de nuevo", category="mensaje--error")
            print("Los passwords no coinciden")

    print("Hiciste una peticion tipo GET")

    return render_template("registrar.html")


@app.route("/usuario/ingresar/", methods=["GET", "POST"])
def ingresar_usuario():
    if request.method == "POST":
        usuario = Usuario.query.filter_by(nombre=request.form["nombre"]).first()

        if usuario and check_password_hash(usuario.password, request.form["password"]):
            flash("Has ingresado exitosamente", category="mensaje--success")
            session["usuario"] = usuario.nombre

            return redirect(url_for("index"))
        else:
            flash("Uno de los datos es incorrecto, vuelve a intentarlo", category="mensaje--error")

    return render_template("ingresar.html")


@app.route("/usuario/salir/")
def salir_usuario():
    session.pop("usuario", None)
    flash("Has cerrado sesion exitosamente", category="mensaje--success")

    return redirect(url_for("index"))


if __name__ == '__main__':
    db.create_all()
    app.run()