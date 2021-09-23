from flask import render_template, url_for, flash, redirect, request
from SheldonsSite import app, db, bcrypt
from SheldonsSite.forms import RegistrationForm, LoginForm, UpdateAccountForm
from SheldonsSite.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

course = [
    {
    'id':0,
    'course': 'Software Defined Networking',
    'school': 'Florida State College at Jacksonville',
    'instructor': 'Sheldon Swanson'
    }
]

sheldon = {
    'firstName': 'Sheldon',
    'lastName': 'Swanson',
    'age': '33'
}

credentials = [
    {
    'name': 'Master of Science',
    'focus': 'Digitial Forensics',
    'from': 'University of South Florida'
    },
    {
    'name': 'Bachelor of Science',
    'focus': 'Computer Networking and Telecomunications',
    'from': 'Florida State Collge at Jacksonville'
    },
    {
    'name': 'Associate of Arts',
    'focus': 'General Education',
    'from': 'Florida State College at Jacksonville'
    },
    {
    'name': 'Master Training Specialist',
    'focus': 'Adult Learning, Curiculum Development, Public Speaking',
    'from': 'Naval Education Center for Professional Development'
    }
]

certifications = [
    {
    'name': 'Fortinet Network Security Expert Level 4',
    'organization': 'Fortinet',
    'Status': 'Active',
    'Expiration Date': ''
    },
    {
    'name': 'Cisco Certified Networking Profesional Enterprise Core',
    'organization': 'Cisco Systems',
    'Status': 'Active',
    'Expiration Date': ''
    },
    {
    'name': 'Security+',
    'organization': 'CompTIA',
    'Status': 'Active',
    'Expiration Date': ''
    },
    {
    'name': 'Network+',
    'organization': 'CompTIA',
    'Status': 'Active',
    'Expiration Date': ''
    },
    {
    'name': 'A+',
    'organization': 'CompTIA',
    'Status': 'Active',
    'Expiration Date': ''
    }
]

schools = [
    {
    'name': 'University of South Florida',
    'area': 'Cybersecurity',
    'focus': 'Digital Forensics'
    },
    {
    'name': 'Florida State College at Jacksonville',
    'area': 'Information Technology',
    'focus': 'Computer Networking'
    },
    {
    'name': 'Naval Education Professional Development Center',
    'area': 'Instructor School',
    'focus': 'Adult Education, Public Speaking, & Curriculum Development'
    },
    {
    'name': 'Naval Education Center for Security Forces',
    'area': 'Small Arms Marksmanship Instructor',
    'focus': ''
    },
    {
    'name': 'Naval Education Center for Security Forces',
    'area': 'Visit Board Search and Seizure Team Member',
    'focus': ''
    },
    {
    'name': 'Naval Education AEGIS Training and Readiness Center',
    'area': 'MK 99 Fire Control System, 400Hz Converter System,\
    Operational Readiness Test System Techician',
    'focus': ''
    },
    {
    'name': 'Naval Education Center for Surface Combat Systems',
    'area': "Firecontrolman 'A' School",
    'focus': ''
    },
    {
    'name': 'Naval Education Advanced Technology Training',
    'area': 'Advanced Technical Training',
    'focus': ''
    }
]

proto = [
    {
    'id':0,
    'name': 'Domain Name System',
    'acron': 'DNS',
    'port': '53',
    'osi': 'application layer',
    'rfc': '1035',
    'purpose': 'Name and IP Address resolution'
    },
    {
    'id':1,
    'name': 'Dynamic Host Control Protocol',
    'acron': 'DHCP',
    'port': '67',
    'osi': 'application layer',
    'rfc': '2131',
    'purpose': 'Dynamic allocation of IP addresses to end hosts'
    },
    {
    'id':2,
    'name': 'File Transfer Protocol',
    'acron': 'FTP',
    'port': '21',
    'osi': 'application layer',
    'rfc': '959',
    'purpose': 'Transfer Files'
    },
    {
    'id':3,
    'name': 'Hypertext Transfer Protocol',
    'acron': 'HTTP',
    'port': '80',
    'osi': 'application layer',
    'rfc': '2616',
    'purpose': 'Delivers Hypertext media to web clients'
    }
]


@app.route('/', methods=['GET'])

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/protocols')
def protocols():
    return render_template('protocols.html', title='Protocols', proto=proto)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form )

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login Success!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form )

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash(f'You have been logged out!', 'success')
    return redirect(url_for('home'))

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/api/all', methods=['GET'])
def api_all():
    return jsonify(course)

@app.route('/api/protocols', methods=['GET'])
def api_protocols():
    return jsonify(protocols)
