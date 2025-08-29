from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from flask_login import current_user, UserMixin, LoginManager, login_required, logout_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, time

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or 'dev-secret-key'
app.config['SESSION_PERMANENT'] = False
print("SECRET_KEY = ", os.getenv("SECRET_KEY"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# User model for storing user data


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

# Movie model for storing movie details


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    cinema = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Movie {self.title}>'

# Reservation model


class Rezerwacja(db.Model):
    __tablename__ = 'Rezerwacja'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    row = db.Column(db.String(100), nullable=False)
    seat = db.Column(db.Integer, nullable=False)
    film = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    sala = db.Column(db.String(100), nullable=False)
    data_rezerwacji = db.Column(db.Date, nullable=False)
    data_wygasania = db.Column(db.Date, nullable=False)
    kinoteatr = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey(
        'show_time.id'), nullable=False)
    # Relationships
    showtime = db.relationship('ShowTime')
    movie = db.relationship('Movie', backref='reservations')
    #  Ensure unique seat per showing
    __table_args__ = (
        UniqueConstraint('row', 'seat', 'film', 'sala',
                         'data_rezerwacji', 'showtime_id', name='unique_seat_per_showing'),
    )

# Showtime model for movie screening times


class ShowTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    movie = db.relationship(
        'Movie', backref=db.backref('showtimes', lazy=True))

    def __repr__(self):
        return f'<ShowTime {self.time} for Movie {self.movie.title}>'


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey(
        'show_time.id'), nullable=False)
    data_rezerwacji = db.Column(db.Date, nullable=False)
    kinoteatr = db.Column(db.String(100), nullable=False)

    showtime = db.relationship('ShowTime', backref='histories')
    movie = db.relationship('Movie', backref='histories')
    user = db.relationship('User', backref='histories')


# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Load user by ID


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page / Link for a home page


@app.route('/')
def home():
    return render_template('index.html')

# User signup function


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')

        if fullname and email and password:
            hashed_password = generate_password_hash(password)
            new_user = User(fullname=fullname, email=email,
                            password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            print("Form data:", request.form)
            return redirect(url_for('home'))
        else:
            return 'Plesse fill everything!'
    return render_template('signup.html')

# User login function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            print("LOGGED IN:", current_user.is_authenticated)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
            return render_template('login.html')
    return render_template('login.html')

# logout. Works only if user logged in


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Contact Page


@app.route('/contact')
def contact():
    return render_template('contact.html')

# Movies page, where displayed can find all the films


@app.route('/movies')
def movies():
    sort_by = request.args.get('sort', 'title')
    movie_list = Movie.query.all()

    # Bubble sort
    if sort_by == 'price':
        n = len(movie_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if movie_list[j].price > movie_list[j + 1].price:
                    movie_list[j], movie_list[j +
                                              1] = movie_list[j + 1], movie_list[j]
    elif sort_by == 'title':
        # Sort by title.
        movie_list.sort(key=lambda movie: movie.title.lower())
    return render_template('movies.html', movies=movie_list)

# Movie details page.


@app.route('/movieDetails/<int:movie_id>')
def movieDetails(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_details.html', movie=movie, datetime=datetime)

# Reserve ticket for a movie. Can't make reservation if reservation is already exist


@app.route('/reserve/<int:movie_id>', methods=['POST'])
def reserve_ticket(movie_id):

    name = request.form.get('name')
    seat = request.form.get('seat')
    row = request.form.get('row')
    sala = request.form.get('hall')
    date_str = request.form.get('date')
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    if date < datetime.today().date():
        flash('You cannot reserve a ticket for a past date.', 'error')
        return redirect(url_for('movieDetails', movie_id=movie_id))
    kinoteatr = request.form.get('cinema')
    showtime_id = int(request.form.get('showtime_id'))
    if not current_user.is_authenticated:
        flash('You must be logged in to reserve a ticket.',
              'error')
        return redirect(url_for('login'))

    existing_reservation = Rezerwacja.query.filter_by(
        row=row,
        seat=seat,
        film=movie_id,
        sala=sala,
        data_rezerwacji=date
    ).first()
    if existing_reservation:
        flash(
            'This seat is already reserved for the selected date. Please choose another seat.', 'error')
        return redirect(url_for('movieDetails', movie_id=movie_id))
        # Creating a reservatiion, and adding to database
    if name and seat and row and sala and date and kinoteatr and showtime_id:
        new_rezerwacja = Rezerwacja(
            name=name,
            seat=seat,
            row=row,
            film=movie_id,
            sala=sala,
            data_rezerwacji=date,
            data_wygasania=date + timedelta(days=1),
            kinoteatr=kinoteatr,
            showtime_id=showtime_id,
            user_id=current_user.id)

        add_to_history = History(
            user_id=current_user.id,
            movie_id=movie_id,
            showtime_id=showtime_id,
            data_rezerwacji=date,
            kinoteatr=kinoteatr
        )

        db.session.add(new_rezerwacja)
        db.session.add(add_to_history)
        db.session.commit()
        flash('Ticket reserved successfully!', 'success')
        return redirect(url_for('movieDetails', movie_id=movie_id))

# Profile page where you can find your reservations and cancel them.


@app.route('/profile')
@login_required
def profile():
    today = datetime.today().date()
    expired_reservations = Rezerwacja.query.filter(  # deleting reservation from profile, if reservation is expired.
        Rezerwacja.data_wygasania < today,
        Rezerwacja.user_id == current_user.id
    ).all()

    for res in expired_reservations:
        db.session.delete(res)
    db.session.commit()

    reservations = Rezerwacja.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', reservations=reservations)

# Cancel reservation function.


@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = Rezerwacja.query.get_or_404(reservation_id)

    if reservation.name != current_user.fullname:
        flash("You can't cancell the reservation.", 'error')
        return redirect(url_for('profile'))

    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation cancelled succesfully!', 'success')
    return redirect(url_for('profile'))

# History function. basicly we're just going through the data base, and show it in the page.


@app.route('/history')
@login_required
def history():
    user_id = current_user.id
    history_records = History.query.filter_by(user_id=user_id).all()
    return render_template('history.html', histories=history_records)


# Creating a tables, that are not created yet.
# with app.app_context():
#     db.create_all()

# with app.app_context():
#     movies = Movie.query.all()
#     times = [time(12, 0), time(15, 0), time(18, 0), time(21, 0)]

#     for movie in movies:
#         for t in times:
#             showtime = ShowTime(time=t, movie_id=movie.id)
#             db.session.add(showtime)
#     db.session.commit()


# Starting app.
if __name__ == '__main__':
    app.run(debug=True)
