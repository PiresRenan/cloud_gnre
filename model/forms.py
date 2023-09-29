from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL, InputRequired

from datetime import date


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    confirm_pass = PasswordField("Confirmar Senha", validators=[DataRequired()])
    name = StringField("Nome", validators=[DataRequired()])
    submit = SubmitField("Cadastrar")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember_me = BooleanField("Lembrar-me")
    submit = SubmitField("Entrar")
    new_user = SubmitField("Novo Usuario")
    recover_password = SubmitField("Recuperar Senha")


class DateFormForGNRE(FlaskForm):
    start_date = DateField('Data Inicial', validators=[DataRequired()])
    end_date = DateField('Data Final', default=date.today(), validators=[DataRequired()])
    submit = SubmitField("Enviar")


class GNREUnico(FlaskForm):
    nf_number = StringField('Numero Nota', validators=[InputRequired()])
    submit = SubmitField("Enviar")
