from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    

class SignUpForm(FlaskForm):
    first_name = StringField("first_name" , validators = [DataRequired()])
    last_name = StringField("last_name", validators = [DataRequired()])
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [Length(min = 6)])
    email = StringField("email", validators = [DataRequired(), Email()])
    image_url = StringField("image_url")
    


class LoginForm(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [Length(min = 6)])

class SendEmailForm(FlaskForm):
    send_to = StringField("send_to", validators = [DataRequired(), Email()])
    # send_from = StringField("send_From", validators = [DataRequired(), Email()])
    subject = TextAreaField("content", validators = [DataRequired()])
    content = TextAreaField("content", validators = [DataRequired()])