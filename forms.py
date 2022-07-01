from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    
    email = StringField("Email: ", validators=[Email("Incorrect email")])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100, message="Password must be between 4 and 100 characters long")])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    
    name = StringField("Name: ", validators=[Length(min=4, max=100, message="Name must be between 4 and 100 characters long")])
    email = StringField("Email: ", validators=[Email("Incorrect email")])
    psw = PasswordField("Password: ", validators=[DataRequired(),
                                                Length(min=4, max=100,
                                                       message="Password must be between 4 and 100 characters long")])

    psw2 = PasswordField("Repeat password: ", validators=[DataRequired(), EqualTo('psw', message="The passwords don't match")])
    submit = SubmitField("Email - registration")