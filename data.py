from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import base64
from flask import session
from flask import jsonify
from flask import redirect
from flask import url_for




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hailmary@localhost/easy'
db = SQLAlchemy(app)

# Define a model for the database table
class FormData(db.Model):
    __tablename__ = 'vregister'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255))
    mname = db.Column(db.String(255))
    lname = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    vehicle = db.Column(db.String(255))
    year = db.Column(db.Integer)
    idpassport = db.Column(db.LargeBinary)
    carreg = db.Column(db.LargeBinary)
    photo1 = db.Column(db.LargeBinary)
    photo2 = db.Column(db.LargeBinary)
    submissionDate = db.Column(db.DateTime)

# Define a model for the booking table
class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    pickup_date = db.Column(db.Date, nullable=False)
    pickup_location = db.Column(db.String(255), nullable=False)
    dropoff_date = db.Column(db.Date, nullable=False)
    dropoff_location = db.Column(db.String(255), nullable=False)
    vehicle_type = db.Column(db.String(255), nullable=False)

    def __init__(self, pickup_date, pickup_location, dropoff_date, dropoff_location, vehicle_type):
        self.pickup_date = pickup_date
        self.pickup_location = pickup_location
        self.dropoff_date = dropoff_date
        self.dropoff_location = dropoff_location
        self.vehicle_type = vehicle_type



#This code defines a new User class that inherits from db.Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


@app.route('/easy')
def home():
    return render_template('index.html')

@app.route('/vehicles')
def vehicles():
    return render_template('vehicles.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')

@app.route('/VehicelRegistration')
def VehicelRegistration():
    return render_template('VehicelRegistration.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/AmdinRegistration')
def AmdinRegistration():
    return render_template('AmdinRegistration.html')


@app.route('/admin')
def admin():
    return render_template('AdminPage.html')

#check if the provided email and password match
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return 'success'
    else:
        return 'failure'

#check if the password and comfirmpassword match and add new user in datanase
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        confirm_pass = request.form['confirm-pass']
        if password == confirm_pass:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return 'Email already taken!'
            else:
                user = User(email=email, password=password)
                db.session.add(user)
                db.session.commit()
                return 'Registration successful!'
        else:
            return 'Password and Confirm Password must be identical!'
    return render_template('AmdinRegistration.html')

#route for handling booking
@app.route('/search-vehicle', methods=['POST'])
def search_vehicle():
    data = request.get_json()
    pickup_date = data['pickup_date']
    pickup_location = data['pickup_location']
    dropoff_date = data['dropoff_date']
    dropoff_location = data['dropoff_location']
    vehicle_type = data['vehicle_type']

    # check if booking is available
    booking = Booking.query.filter_by(pickup_date=pickup_date, pickup_location=pickup_location, dropoff_date=dropoff_date, dropoff_location=dropoff_location, vehicle_type=vehicle_type).first()
    if booking:
        # booking already exists
        return jsonify({'status': 'error', 'message': 'Already booked'})
    else:
        # create new booking
        new_booking = Booking(pickup_date=pickup_date, pickup_location=pickup_location, dropoff_date=dropoff_date, dropoff_location=dropoff_location, vehicle_type=vehicle_type)
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Successfully booked'})


@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Get the form data from the POST request
    fname = request.form['fname']
    mname = request.form['mname']
    lname = request.form['lname']
    phone = request.form['phone']
    email = request.form['email']
    vehicle = request.form['vehicle']
    year = request.form['year']

    # Get the values of the new form fields for ID/Passport,Car Registration,car photo
    idpassport = request.files['idpassport'].read()
    carreg = request.files['carreg'].read()
    photo1 = request.files['photo1'].read()
    photo2 = request.files['photo2'].read()
    # Get the current date and time
    currentDate = datetime.now()

    # Create a new FormData object with the form data
    form_data = FormData(
        fname=fname,
        mname=mname,
        lname=lname,
        phone=phone,
        email=email,
        vehicle=vehicle,
        year=year,
        idpassport=idpassport,
        carreg=carreg,
        photo1=photo1,
        photo2=photo2,
        submissionDate=currentDate
    )

    # Add the new FormData object to the database session and commit the changes
    db.session.add(form_data)
    db.session.commit()

    return 'Data inserted successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)