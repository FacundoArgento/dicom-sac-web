from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_simple_captcha import CAPTCHA

# Config
from config import config

# Models
from models.ModelUser import ModelUser
from models.ModelInstitution import ModelInstitution

# Entities
from models.entities.User import User

app = Flask(__name__)

#CAPTCHA = CAPTCHA(config=config['development'].CAPTCHA_CONFIG)
#app = CAPTCHA.init_app(app)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.getById(db, id)

# Routes
@app.route('/')
def index():
    if current_user != None:
        return redirect(url_for('form'))
    else:
        #captcha = CAPTCHA.create()
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                if logged_user.active:
                    login_user(logged_user)
                    return redirect(url_for('form'))
                else:
                    flash(f"El usuario '{user.username}' no esta activo para la carga de datos.")
                    return render_template('auth/login.html')
            else:
                flash("Contraseña inccorrecta..")
                return render_template('auth/login.html')
        else:
            flash("No existe el usuario indicado.")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    #captcha = CAPTCHA.create()
    return redirect(url_for('login'))


@app.route('/form', methods = ['GET','POST'])
@login_required
def form():
    if request.method == 'POST':
        print("hola")
        # funcionalidad subida de dicoms
    else:    
        institutions = ModelInstitution.getAllInstitutions(db)
        return render_template('/form.html', institutions = institutions)

# Status errors

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

# main

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()