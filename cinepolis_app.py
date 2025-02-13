from flask import Flask, render_template, request

app = Flask(__name__)

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

        total = round(total, 2)

        self.total_corte += total
        self.compras.append((nombre, boletos, total))

        return total

    def calcular_total(self, boletos):
        precio_unitario = 12
        if boletos > 5:
            descuento = 0.15
        elif 3 <= boletos <= 5:
            descuento = 0.10
        else:
            descuento = 0

        total = boletos * precio_unitario * (1 - descuento)
        return total

    def terminar_programa(self):
       
        resumen_lista = []
        for compra in self.compras:
            nombre, boletos, total = compra
            resumen_lista.append([nombre, boletos, f"${total:.2f}"]) 

       
        total_general = f"${self.total_corte:.2f}"

        return resumen_lista, total_general 

    def validar_personas(self, personas):
        try:
            personas = int(personas)
            if 1 <= personas <= 7:
                return personas
            else:
                return None  
        except ValueError:
            return None  

    def validar_boletos(self, boletos):
        try:
            boletos = int(boletos)
            if boletos <= 0:
                return None  
            elif boletos > self.personas:  
                return None  
            elif self.personas > boletos:
                return None
            elif boletos < 1: 
                return None  
            else:
                return boletos
        except ValueError:
            return None   


cinepolis = Cinepolis()

@app.route("/", methods=["GET", "POST"])
def index():
    total = None
    resumen = None
    total_general = None
    error_personas = None
    error_boletos = None

    if request.method == "POST":
        nombre = request.form.get("nombre")
        personas_input = request.form.get("personas")
        boletos_input = request.form.get("boletos")
        tarjeta = request.form.get("tarjeta")

        personas = cinepolis.validar_personas(personas_input)
        if personas is None:
            error_personas = "Deben ser entre 1 y 7 personas."
        else: 
            cinepolis.personas = personas  
            boletos = cinepolis.validar_boletos(boletos_input)
            if boletos is None:
                error_boletos = "La cantidad de boletos no coincide con la cantidad de personas."

        if personas is not None and boletos is not None:
            total = cinepolis.realizar_compra(nombre, personas, boletos, tarjeta)

    elif request.method == "GET" and request.args.get("terminar"):
        resumen, total_general = cinepolis.terminar_programa()

    return render_template("cinepolis.html", total=total, resumen=resumen, 
                           total_general=total_general, error_personas=error_personas,
                           error_boletos=error_boletos)

if __name__ == "__main__":
    app.run(debug=True)