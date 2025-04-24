from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, UserMixin, LoginManager, login_required, logout_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or 'dev-secret-key'
app.config['SESSION_PERMANENT'] = False
print("SECRET_KEY = ", os.getenv("SECRET_KEY"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    cinema = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Movie {self.title}>'


class Rezerwacja(db.Model):
    __tablename__ = 'Rezerwacja'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    row = db.Column(db.String(100), nullable=False)
    seat = db.Column(db.Integer, nullable=False)
    film = db.Column(db.Integer, nullable=False)
# film, sala, godzina, kinoteatr, data_wygasania, data_rezerwacji


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('index.html')


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
            return 'Будь ласка, заповни всі поля!'
    return render_template('signup.html')


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


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/movies')
def movies():
    # за замовчуванням сортування за назвою
    sort_by = request.args.get('sort', 'title')
    movie_list = Movie.query.all()

    # Bubble sort за ціною
    if sort_by == 'price':
        n = len(movie_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if movie_list[j].price > movie_list[j + 1].price:
                    movie_list[j], movie_list[j +
                                              1] = movie_list[j + 1], movie_list[j]
    elif sort_by == 'title':
        # Сортування за назвою вручну (якщо треба)
        movie_list.sort(key=lambda movie: movie.title.lower())
    return render_template('movies.html', movies=movie_list)


@app.route('/movieDetails/<int:movie_id>')
def movieDetails(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_details.html', movie=movie)


@app.route('/reserve/<int:movie_id>', methods=['POST'])
def reserve_ticket(movie_id):
    movie_list = Movie.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        seat = request.form.get('seat')
        row = request.form.get('row')
        movie = request.form.get(movie_id)
        if name and seat and row:
            new_rezerwacja = Rezerwacja(
                name=name, seat=seat, row=row, film=movie_id)
            db.session.add(new_rezerwacja)
            db.session.commit()
            print(
                f'{name} забронював(ла) місце {seat} ряд {row} на фільм з ID {movie_id}')
    # Тут можна зберігати в базу або просто вивести
    return render_template('signup.html')  # або показати підтвердження


# with app.app_context():
    # db.create_all()


# with app.app_context():
   # User.query.delete()
    # db.session.commit()
    # print("Всі користувачі видалені.")


if __name__ == '__main__':
    app.run(debug=True)


# with app.app_context():
    # db.create_all()
