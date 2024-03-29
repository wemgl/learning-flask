from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, SigninForm, AddressForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/learningflask'

db.init_app(app)

app.secret_key = "development-key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    form = SignupForm()
    if request.method == 'GET':
        return render_template("signup.html", form=form)

    if not form.validate_on_submit():
        return render_template("signup.html", form=form)

    newuser = User(firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data,
                   password=form.password.data)
    db.session.add(newuser)
    db.session.commit()

    session['email'] = newuser.email

    return redirect(url_for('home'))


@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('signin'))

    form = AddressForm()
    places = []
    my_coordinates = (37.4221, -122.0844)

    if request.method == 'GET':
        return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

    if not form.validate_on_submit():
        return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

    # get the address
    address = form.address.data

    # query for places around it
    p = Place()
    my_coordinates = p.address_to_latlng(address)
    places = p.query(address)

    # return those results
    return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if 'email' in session:
        return redirect(url_for('home'))

    form = SigninForm()
    if request.method == 'GET':
        return render_template("signin.html", form=form)

    if not form.validate_on_submit():
        return render_template("signin.html", form=form)

    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password=password):
        session['email'] = email
        return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))


@app.route("/signout")
def signout():
    session.pop('email', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
