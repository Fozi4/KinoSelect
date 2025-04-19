from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#  Головна сторінка


@app.route('/')
def home():
    return render_template('index.html')

#  Сторінка реєстрації


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        # тимчасово просто виводимо
        print(f"Новий користувач: {fullname}, {email}, {password}")
        return redirect(url_for('login'))
    return render_template('signup.html')

#  Сторінка входу


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # тимчасово просто виводимо
        print(f"Спроба входу: {email}, {password}")
        return redirect(url_for('home'))
    return render_template('login.html')

#  Сторінка контактів


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
