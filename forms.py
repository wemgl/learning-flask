from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired('Please enter your first name')])
    last_name = StringField('Last Name', validators=[DataRequired('Please enter your last name')])
    email = StringField('E-mail', validators=[DataRequired('Please enter your e-mail address'),
                                              Email("Please enter a valid email address")])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password'),
                                                     Length(min=6,
                                                            message="Your password must be longer than 6 characters")])
    submit = SubmitField('Sign up')
