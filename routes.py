from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Event
from forms import RegisterForm, LoginForm, EventForm

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('routes.register'))

        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            first_name=form.first_name.data,
            surname=form.surname.data,
            email=form.email.data,
            password_hash=hashed_pw,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)
@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('routes.index'))
        flash("Invalid email or password.")
    return render_template('login.html', form=form)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@routes.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
    title=form.title.data,
    description=form.description.data,
    date=form.date.data.strftime("%Y-%m-%d") if form.date.data else "",
    start_time=form.start_time.data.strftime("%H:%M") if form.start_time.data else "",
    end_time=form.end_time.data.strftime("%H:%M") if form.end_time.data else "",
    location=form.location.data,
    ticket_price=form.ticket_price.data,
    ticket_amount=form.ticket_amount.data,
    status=form.status.data,
    artist_info=form.artist_info.data
)
        db.session.add(event)
        db.session.commit()
        flash("Event created successfully.")
        return redirect(url_for('routes.index'))
    return render_template('create.html', form=form)

@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/bookings')
@login_required
def bookings():
    return render_template('booking.html')

