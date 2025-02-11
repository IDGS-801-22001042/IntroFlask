from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    titulo="IDGS801"
    lista=["pedro","juan","luis"]
    return render_template("index.html",titulo= titulo,lista=lista)

@app.route("/ejemplo1")
def ejemplo1():
    return render_template("ejemplo1.html")    

@app.route("/ejemplo2")
def ejemplo2():
    return render_template("ejemplo2.html")  

@app.route("/hola")
def hola():
    return "<h1>Hola, mundo---Hola--</h1>"

if __name__ == "__main__":
    app.run(debug=True, port=3000)

@app.route("/user/<string:user>")
def user(user):
    print(f"User function called with: {user}")  # Add this line
    return f"<h1>Hello {user}</h1>"

@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El número es: {FileNotFoundError}</h1>"

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return f"<h1>Hello {username}, ¡Tu ID es: {id}!</h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1,n2):
    return f"<h1>La suma es: {n1+n2}</h1>"

@app.route("/default/")
@app.route("/default/<string:param>")
def c(param="Juan"):
    return f"<h1>Hola, {param}</h1>"

@app.route("/operas")
def operas():
    return '''<form action="procesar.php" method="post">
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre" required>
            <br><br>
            
            <label for="apellidos">Apellidos:</label>
            <input type="text" id="apellidos" name="apellidos" required>
            <br><br>
            
            <button type="submit">Enviar</button>
        </form>'''