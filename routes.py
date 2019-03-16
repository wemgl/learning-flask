from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm

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


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
