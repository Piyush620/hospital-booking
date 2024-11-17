from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from flask_mail import Mail, Message
import json

with open('config.json','r') as c:
    piyush = json.load(c)["piyush"]

# Initialize Flask app
local_server = True
app = Flask(__name__)
app.secret_key = 'Piyush'  # Replace this with a secure key in production

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# SMTP Mail server settings
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=piyush['gmail-user'],
    MAIL_PASSWORD=piyush['gmail-password'],
    MAIL_DEFAULT_SENDER=piyush['gmail-user']  # Ensure the default sender is set to your Gmail user
)
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/hms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))

class Patients(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    slot = db.Column(db.String(50))
    disease = db.Column(db.String(50))
    time = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50))  # Allow dept to be nullable
    number = db.Column(db.String(50))

class Doctors(db.Model):
    did = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    doctorname = db.Column(db.String(100))
    dept = db.Column(db.String(50))  # Add the dept column

# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/doctors', methods=['POST', 'GET'])
def doctors():
    if request.method == "POST":
        email = request.form.get('email')
        doctorname = request.form.get('doctorname')
        dept = request.form.get('dept')

        try:
            new_doctor = Doctors(email=email, doctorname=doctorname, dept=dept)
            db.session.add(new_doctor)
            db.session.commit()
            flash("Doctor information has been stored.", "primary")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")

    return render_template('doctors.html')


@app.route('/patients', methods=['POST', 'GET'])
@login_required
def patients():
    doctors = Doctors.query.all()
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        gender = request.form.get('gender')
        slot = request.form.get('slot')
        disease = request.form.get('disease')
        time = request.form.get('time')
        date = request.form.get('date')
        dept = request.form.get('dept')
        number = request.form.get('number')
        new_patient = Patients(
            email=email,
            name=name,
            gender=gender,
            slot=slot,
            disease=disease,
            time=time,
            date=date,
            dept=dept,
            number=number
        )

        try:
            db.session.add(new_patient)
            db.session.commit()
            flash("Booking Confirmed", "info")
            return redirect(url_for('bookingdetails'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
        
        # Sending confirmation email using Flask-Mail
        try:
            msg = Message('HOSPITAL MANAGEMENT SYSTEM',
                          recipients=[piyush['gmail-user']],
                          body='YOUR BOOKING IS CONFIRMED. THANKS FOR CHOOSING US!')
            mail.send(msg)
            flash("Booking Confirmed", "info")
        except Exception as e:
            flash(f"An error occurred while sending email: {str(e)}", "danger")
    return render_template('patients.html', doct=doctors)


@app.route('/bookingdetails')
@login_required
def bookingdetails():
    em = current_user.email
    bookings_details = Patients.query.filter_by(email=em).all()
    return render_template('bookingdetails.html', query=bookings_details)


@app.route("/edit/<string:pid>", methods=['POST', 'GET'])
@login_required
def edit(pid):
    posts = Patients.query.filter_by(pid=pid).first()
    if not posts:
        flash("No patient record found", "danger")
        return redirect(url_for('bookingdetails'))

    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        gender = request.form.get('gender')
        slot = request.form.get('slot')
        disease = request.form.get('disease')
        time = request.form.get('time')
        date = request.form.get('date')
        dept = request.form.get('dept')
        number = request.form.get('number')

        try:
            posts.email = email
            posts.name = name
            posts.gender = gender
            posts.slot = slot
            posts.disease = disease
            posts.time = time
            posts.date = date
            posts.dept = dept
            posts.number = number

            db.session.commit()
            flash("Slot is updated", "success")
            return redirect(url_for('bookingdetails'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('edit', pid=pid))

    return render_template('edit.html', posts=posts)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful", "primary")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", "warning")
            return render_template('signup.html')

        encpassword = generate_password_hash(password)
        new_user = User(username=username, email=email, password=encpassword)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Signup Successful. Please log in.", "success")
            return redirect(url_for('login'))
        except SQLAlchemyError:
            db.session.rollback()
            flash("An error occurred during signup. Please try again.", "danger")
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful", "warning")
    return redirect(url_for('login'))


@app.route("/delete/<int:pid>", methods=['POST'])
@login_required
def delete(pid):
    try:
        patient = Patients.query.get_or_404(pid)
        if patient.email != current_user.email:
            flash("You are not authorized to delete this record", "danger")
            return redirect(url_for('bookingdetails'))
        
        db.session.delete(patient)
        db.session.commit()
        flash("Booking deleted successfully", "danger")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
    
    return redirect(url_for('bookingdetails'))


# Run the app
if __name__ == '__main__':
    app.run(debug=True)