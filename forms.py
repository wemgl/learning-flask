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


class SigninForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(message="Please enter your email to login"),
                                              Email(message="Please enter your email address")])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter your password to login")])
    submit = SubmitField('Sign in')


class AddressForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired(message="Please enter an address")])
    submit = SubmitField('Search')
