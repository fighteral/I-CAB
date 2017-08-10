_author__ = "Rishav Gupta, Pawan Patil,Pranav Salathia, Parth Sharma"
__copyright__ = "Copyright (C) 2016 Rishav Gupta"
__license__ = "Public Domain"
__version__ = "1.0"




from flask import Flask,render_template,request,url_for,flash,session,redirect
from flask_session import Session
from dbconnect import connection
from wtforms import Form,BooleanField,StringField,TextField,PasswordField,validators,IntegerField,RadioField
from passlib.hash import sha256_crypt
from wtforms.fields.html5 import EmailField
from MySQLdb import escape_string as thwart
from flask_wtf import Form
from wtforms.validators import  InputRequired,Regexp
import gc
from geolocation.main import GoogleMaps
import geolocation.distance_matrix
from functools import wraps
from flask_wtf.csrf import CsrfProtect


sess=Session()
SESSION_TYPE = 'memcache'
app=Flask(__name__)


csrf = CsrfProtect()

def create_app():
    app.secret_key = 'super secret key'
    app = Flask(__name__)
    csrf.init_app(app)


@app.route('/')
def test():
    return render_template("home1.html")


@app.route('/about/')
def about():
    return render_template("about.html")

class BookingForm(Form):
    start=StringField('Starting Address',[validators.Required()])
    destination=TextField('Destination',[validators.Required()])
class BookingForm1(Form):
    start=StringField('Starting Address',[validators.Required()])
    destination=TextField('Destination',[validators.Required()])
class BookingForm2(Form):
    start=StringField('Starting Address',[validators.Required()])
    destination=TextField('Destination',[validators.Required()])
class BookingForm3(Form):
    start=StringField('Starting Address',[validators.Required()])
    destination=TextField('Destination',[validators.Required()])


def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("you need to login first")
            return redirect(url_for('login'))
    return wrap


@app.route('/Sedan/',methods=['GET','POST'])
@login_required
def sedan():
    form=BookingForm2(request.form)
    try:
        if request.method == 'POST':
            start=form.start.data
            destination=form.destination.data
            start = request.form['start']
            destination = request.form['destination']
            gmaps = GoogleMaps('Your goolge key')
            start =start
            end   = destination
            dirs  = gmaps.distance(start, end)

            for step in dirs:
                x=str(float(step.distance.kilometers))
                z=float(x)
                if z>50.0:
                    flash("Distance is more than 50 km.Please change the credentials")
                else:

                    y=str(z*float(4))
                    flash("Distance is:"+x)
                    flash("Total fare is :" +y)

    except Exception as e:
        flash("Please enter the credentials or check your internet connecton")
    return render_template("sedan.html",form=form)

@app.route('/SedanA.C./',methods=['GET','POST'])
@login_required
def sedana():
    form=BookingForm2(request.form)
    try:
        if request.method == 'POST':
            start=form.start.data
            destination=form.destination.data
            start = request.form['start']
            destination = request.form['destination']
            gmaps = GoogleMaps('Your goolge key')
            start =start
            end   = destination
            dirs  = gmaps.distance(start, end)
            for step in dirs:
                x=str(float(step.distance.kilometers))
                z=float(x)
                if z>50.0:
                    flash("Distance is more than 50 km.Please change the credentials")
                else:

                    y=str(z*float(7))
                    flash("Distance is:"+x)
                    flash("Total fare is :" +y)

    except Exception as e:
        flash("Please enter the credentials or check your internet connecton")

    return render_template("sedanac.html",form=form)

@app.route('/SUV/',methods=['GET','POST'])
@login_required
def suv():
    form=BookingForm2(request.form)
    try:
        if request.method == 'POST':
            start=form.start.data
            destination=form.destination.data
            start = request.form['start']
            destination = request.form['destination']
            gmaps = GoogleMaps('Your goolge key')
            start =start
            end   = destination
            dirs  = gmaps.distance(start, end)

            for step in dirs:
                x=str(float(step.distance.kilometers))
                z=float(x)
                if z>50.0:
                    flash("Distance is more than 50 km.Please change the credentials")
                else:

                    y=str(z*float(10))
                    flash("Distance is:"+x)
                    flash("Total fare is :" +y)

    except Exception as e:
        flash("Please enter the credentials or check your internet connecton")
    return render_template("suv.html",form=form)

@app.route('/SUVA.C./',methods=['GET','POST'])
@login_required
def suva():
    form=BookingForm2(request.form)
    try:
        if request.method == 'POST':
            start=form.start.data
            destination=form.destination.data
            start = request.form['start']
            destination = request.form['destination']
            gmaps = GoogleMaps('Your goolge key')
            start =start
            end   = destination
            dirs  = gmaps.distance(start, end)
            for step in dirs:
                x=str(float(step.distance.kilometers))
                z=float(x)
                if z>50.0:
                    flash("Distance is more than 50 km.Please change the credentials")
                else:

                    y=str(z*float(12))
                    flash("Distance is:"+x)
                    flash("Total fare is :" +y)

    except Exception as e:
        flash("Please enter the credentials or check your internet connecton")
    return render_template("suvac.html",form=form)


@app.route('/contact/')
def contact():
    return render_template("contact.html")


@app.route('/cab/')
def cab():
    return render_template("type.html")


@app.route("/logout/")
@login_required
def logout():
    session.clear()

    gc.collect()
    return redirect(url_for('test'))



@app.route('/login/',methods=['GET','POST'])
def login():

    try:
        c,conn =connection()
        if request.method=='POST':
            data =c.execute("SELECT * FROM customer WHERE username=(%s)",
                            (request.form['username'],))
            data=c.fetchone()[3]
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in']=True
                session['username']=request.form['username']

                flash("Welcome!.You are logged in:"+session['username'])
                return redirect(url_for("cab"))
            else:
                flash("Invalid credentials!.Please try again!!")
        gc.collect()
    except Exception as e:
        flash("Internal error")
    return render_template("login.html")




class RegistrationForm(Form):
    username=StringField('Username',[validators.Length(min=4,max=20),validators.Required()])
    email= EmailField('E-mail',[validators.Length(min=6,max=50),validators.Required(),validators.Email()])
    password=PasswordField('Password',[validators.Length(min=6,max=20),validators.EqualTo('confirm',message="Password must match"),validators.Required()])
    confirm=PasswordField("Repeat Password")
    phone_no=StringField('Phone No.',[validators.Length(min=10,message="Please enter correct phone no."),validators.Required()])



@app.route("/sign_up/",methods=['GET','POST'])
def sign():
    form=RegistrationForm(request.form)
    if request.method == 'POST' and form.validate() :
        username=form.username.data
        email=form.email.data
        password=sha256_crypt.encrypt((str(form.password.data)))
        phone_no=form.phone_no.data
        c,conn =connection()


        x = c.execute("SELECT * FROM customer WHERE username =(%s)",
                        (username,))

        if int(x)>0:
            flash("That username is taken.Please choose another username")
            return render_template('sign.html',form=form)
        else:

            c.execute("INSERT INTO customer (username,email,password,phone_no) VALUES (%s,%s,%s,%s)",
            (thwart(username),thwart(email),thwart(password),thwart(phone_no)))

            conn.commit()
            session['logged_in']=True
            session['username']=username
            flash("Thanks for registering: "+session['username'])

            c.close()
            conn.close()
            gc.collect()

            return redirect(url_for('cab'))
    return render_template("sign.html",form=form)


if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(debug=True)
