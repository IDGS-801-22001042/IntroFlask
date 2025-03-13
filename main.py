from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import forms
from flask_wtf.csrf import CSRFProtect
from flask import flash
from flask import g
from forms import ZodiacoForm

app = Flask(__name__)
app.secret_key="Papitas Con Salsa"
csrf=CSRFProtect()

# -------------------- Funciones Generales --------------------
@app.route("/")
def index():
    nom='None'
    titulo = "IDGS801"
    lista = ["pedro", "juan", "luis"]
    nom = g.user
    print("Index 2 {}".format(g.user))
    return render_template("index.html", titulo=titulo,nom=nom, lista=lista)

@app.route("/ejemplo1")
def ejemplo1():
    return render_template("ejemplo1.html")

@app.route("/ejemplo2")
def ejemplo2():
    return render_template("ejemplo2.html")

@app.route("/hola")
def hola():
    return "<h1>Hola, mundo---Hola--</h1>"

@app.route("/user/<string:user>")
def user(user):
    return f"<h1>Hello {user}</h1>"

@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El número es: {n}</h1>"

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return f"<h1>Hello {username}, ¡Tu ID es: {id}!</h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return f"<h1>La suma es: {n1 + n2}</h1>"

@app.route("/default/")
@app.route("/default/<string:param>")
def c(param="Juan"):
    return f"<h1>Hola, {param}</h1>"

# -------------------- Zodiaco Chino --------------------
@app.route("/Zodiaco", methods=["GET", "POST"])
def zodiaco():
    form = forms.ZodiacoForm(request.form)
    
    if request.method == "POST" and form.validate():
        nombre = form.nombre.data
        apaterno = form.apaterno.data
        amaterno = form.amaterno.data
        dia = form.dia.data
        mes = form.mes.data
        anio = form.anio.data
        
        fecha_nacimiento = datetime(anio, mes, dia)
        hoy = datetime.now()
        edad = hoy.year - fecha_nacimiento.year
        if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1

        signos = [
            "Rata", "Buey", "Tigre", "Conejo", "Dragón", "Serpiente",
            "Caballo", "Cabra", "Mono", "Gallo", "Perro", "Cerdo"
        ]
        imagenes = [
            "rata.png", "buey.png", "tigre.png", "conejo.png", "dragon.png",
            "serpiente.png", "caballo.png", "cabra.png", "mono.png",
            "gallo.png", "perro.png", "cerdo.png"
        ]
        
        indice_signo = (anio - 1900) % 12
        signo = signos[indice_signo]
        img = imagenes[indice_signo]

        resultado = {
            "nombre": nombre,
            "apaterno": apaterno,
            "amaterno": amaterno,
            "edad": edad,
            "signo": signo,
            "img": img
        }

        return render_template("ZodiacoChino.html", form=form, resultado=resultado)

    return render_template("ZodiacoChino.html", form=form)

# -------------------- Operas Básicas --------------------
@app.route("/OperasBas", methods=["GET", "POST"])
def operasBas():
    return render_template("OperasBas.html")

@app.route("/resultado", methods=["POST"])
def res():
    if request.method == "POST":  
        n1 = int(request.form.get("n1", 0))
        n2 = int(request.form.get("n2", 0))
        operacion = request.form.get("operacion")

        if operacion == "multiplicacion":
            result = n1 * n2
        elif operacion == "suma":
            result = n1 + n2
        elif operacion == "resta":
            result = n1 - n2
        elif operacion == "division":
            if n2 == 0:
                return "No se puede dividir por cero."
            result = n1 / n2
        else:
            return "Operación no válida."
        
        return f"El resultado de la {operacion} entre {n1} y {n2} es: {result}"

# -------------------- Alumnos --------------------
@app.route("/Alumnos", methods=["GET", "POST"])
def alumnos():
    mat=""
    nom=""
    ape=""
    email=""
    alumno_class=forms.UserForm(request.form)
    if request.method == "POST" and alumno_class.validate():
        mat = alumno_class.matricula.data
        nom = alumno_class.nombre.data
        ape = alumno_class.apellido.data
        email = alumno_class.correo.data
       
        mensaje = 'Bienvenido {}'.format(nom)
        flash(mensaje) 
        
    return render_template("Alumnos.html", form=alumno_class, mat=mat, nom=nom, ape=ape, email=email)



#-------------------- Manejo de errores -------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    print("BEFORER1")
    return None
    
@app.after_request
def after_request(response):
    print("AFTERR1")
    return response

# -------------------- Cinepolis --------------------
class Cinepolis:
    def __init__(self):
        self.compras = []
        self.total_corte = 0.0
        self.personas = 0

    def realizar_compra(self, nombre, personas, boletos, tarjeta):
        self.personas = personas
        total = self.calcular_total(boletos)
        if tarjeta == "si":
            total *= 0.9
        self.total_corte += total
        self.compras.append((nombre, boletos, round(total, 2)))
        return total

    def calcular_total(self, boletos):
        precio_unitario = 12
        if boletos > 5:
            descuento = 0.15
        elif 3 <= boletos <= 5:
            descuento = 0.10
        else:
            descuento = 0
        return boletos * precio_unitario * (1 - descuento)

    def terminar_programa(self):
        resumen = [(compra[0], compra[1], f"${compra[2]:.2f}") for compra in self.compras]
        return resumen, f"${self.total_corte:.2f}"

    def validar_personas(self, personas):
        return personas if 1 <= personas <= 7 else None

cinepolis = Cinepolis()

@app.route("/Cinepolis", methods=["GET", "POST"])
def cinepolis_index():
    form = forms.CinepolisForm(request.form)
    total, resumen, total_general = None, None, None

    if request.method == "POST" and form.validate():
        nombre = form.nombre.data
        personas = form.personas.data
        boletos = form.boletos.data
        tarjeta = form.tarjeta.data

        if cinepolis.validar_personas(personas):
            total = cinepolis.realizar_compra(nombre, personas, boletos, tarjeta)
        else:
            flash("Número de personas no válido.", "error")

    elif request.method == "GET" and request.args.get("terminar"):
        resumen, total_general = cinepolis.terminar_programa()

    return render_template("cinepolis.html", form=form, total=total, resumen=resumen, total_general=total_general)

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True, port=3000)