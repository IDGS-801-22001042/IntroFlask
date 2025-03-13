from wtforms import Form, validators, ValidationError
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange

#---------------------Alumnos-------------------------------
class UserForm(Form):
    matricula = IntegerField("Matricula", [
        validators.DataRequired(message='El campo es requerido')
    ])
    nombre = StringField("Nombre", [
        validators.DataRequired(message='El campo es requerido')
    ])
    apellido = StringField("Apellido", [
        validators.DataRequired(message='El campo es requerido')
    ])
    correo = EmailField("Correo", [
        validators.Email(message='Correo invalido')
    ])

#--------------------Form Cinepolis------------------------

class CinepolisForm(Form):
    nombre = StringField("Nombre", [validators.DataRequired(message="Campo requerido")])
    personas = IntegerField("Número de personas", [
        validators.DataRequired(),
        validators.NumberRange(min=1, max=7, message="Debe ser entre 1 y 7 personas")
    ])
    boletos = IntegerField("Número de boletos", [
        validators.DataRequired(),
        validators.NumberRange(min=1, message="Debe ser al menos 1 boleto")
    ])
    tarjeta = RadioField("¿Tarjeta Cineco?", choices=[('si', 'Sí'), ('no', 'No')], validators=[validators.DataRequired()])

    def validate_boletos(self, field):
        if self.personas.data and field.data:
            if field.data < self.personas.data:
                raise ValidationError("Debe comprar al menos un boleto por persona.")
            elif field.data > self.personas.data:
                raise ValidationError("No puede comprar más boletos que personas registradas.")


#--------------------Form Zodiaco------------------------

class ZodiacoForm(Form):
    nombre = StringField("Nombre", [
        DataRequired(message='El campo es requerido')
    ])
    apaterno = StringField("Apellido Paterno", [
        DataRequired(message='El campo es requerido')
    ])
    amaterno = StringField("Apellido Materno", [
        DataRequired(message='El campo es requerido')
    ])
    dia = IntegerField("Día", [
        DataRequired(message='El campo es requerido'),
        NumberRange(min=1, max=31, message='Día no válido')
    ])
    mes = IntegerField("Mes", [
        DataRequired(message='El campo es requerido'),
        NumberRange(min=1, max=12, message='Mes no válido')
    ])
    anio = IntegerField("Año", [
        DataRequired(message='El campo es requerido'),
        NumberRange(min=1910, max=2025, message='Año no válido')
    ])
    sexo = RadioField("Sexo", choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')], 
                      validators=[DataRequired(message='El campo es requerido')])
