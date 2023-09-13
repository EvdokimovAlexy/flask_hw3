from flask import Flask, render_template, request, flash, redirect, url_for, session
import os

from unicodedata import category


from models import db, User2

from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
csrf = CSRFProtect(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///users.db"
db.init_app(app)



@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', category=category)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        name = form.name.data.lower()
        surname = form.surname.data.lower()
        email = form.email.data
        user = User2(name=name, surname=surname, email=email)
        if User2.query.filter(User2.email == email).first():
            flash(f'Пользователь с e-mail {email} уже существует')
            return redirect(url_for('registration'))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Вы успешно зарегистрировались!')
        return redirect(url_for('registration'))
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run()
