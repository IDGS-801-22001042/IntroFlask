from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    titulo = "IDGS801"
    lista = ["pedro", "juan", "luis"]
    return render_template("index.html", titulo=titulo, lista=lista)

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
    print(f"User function called with: {user}")
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

@app.route("/operas")
def operasi():
    return '''<form action="/procesar" method="post">  </form>''' 

@app.route("/Zodiaco", methods=["GET", "POST"])
def zodiaco():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apaterno = request.form.get("apaterno")
        amaterno = request.form.get("amaterno")
        dia = int(request.form.get("dia"))
        mes = int(request.form.get("mes"))
        anio = int(request.form.get("anio"))
        sexo = request.form.get("sexo")

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

        return render_template("ZodiacoChino.html", resultado=resultado)

    return render_template("ZodiacoChino.html")

@app.route("/OperasBas", methods=["GET", "POST"])
def operasBas():
    return render_template("OperasBas.html")

@app.route("/resultado", methods=["GET", "POST"])
def res():
    if request.method == "POST":  
        n1 = request.form.get("n1")
        n2 = request.form.get("n2")
        operacion = request.form.get("operacion")  

        try:
            n1 = int(n1)
            n2 = int(n2)

            if operacion == "multiplicacion":
                result = n1 * n2
                return f"La multiplicación de {n1} y {n2} es: {result}"
            elif operacion == "suma":
                result = n1 + n2
                return f"La suma de {n1} y {n2} es: {result}"
            elif operacion == "resta":
                result = n1 - n2
                return f"La resta de {n1} y {n2} es: {result}"
            elif operacion == "division":
                if n2 == 0:
                    return "No se puede dividir por cero."
                result = n1 / n2
                return f"La división de {n1} y {n2} es: {result}"
            else:
                return "Operación no válida."  

        except (ValueError, TypeError):
            return "Solo números"
    return "Únicamente solicitudes POST" 


if __name__ == "__main__":
    app.run(debug=True, port=3000)