from wtforms import Form, StringField, SelectField, TextField, TextAreaField, validators, SubmitField

class Pessoa(Form):
    nome = StringField(label='nome')
    telefone = StringField(label='telefone')
    dropdown_choices = [('Volvo', 'Volvo'),
               ('Saab', 'Saab'),
               ('Mercedes', 'Mercedes'),
               ('Audi', 'Audi')]
    dropdown = SelectField(choices=dropdown_choices, label='Carro')
    cpf = StringField(label='cpf')
    email = StringField(label='email')
