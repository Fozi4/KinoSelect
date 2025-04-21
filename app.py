from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


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
            new_user = User(fullname=fullname, email=email, password=password)
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
        email = request.form.get('email')
        password = request.form.get('password')

        # Тимчасова перевірка
        if email and password:  # Тут буде реальна перевірка з бази потім
            print("Form data: ", request.form)
            return redirect(url_for('home'))
        else:
            return "Invalid email or password", 401

    return render_template('login.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)


# with app.app_context():
    # db.create_all()
