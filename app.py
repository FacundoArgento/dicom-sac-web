from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_simple_captcha import CAPTCHA

# Config
from config import config
from models.ModelStudy import ModelStudy

# Models
from models.ModelUser import ModelUser
from models.ModelInstitution import ModelInstitution
from models.ModelEquipment import ModelEquipment
from models.ModelDiagnosis import ModelDiagnosis
#from models.ModelStudy import ModelStudy

# Entities
from models.entities.User import User

# Payload
from services.DicomUploader import uploadCompleteStudy, verify

app = Flask(__name__)

#CAPTCHA = CAPTCHA(config=config['development'].CAPTCHA_CONFIG)
#app = CAPTCHA.init_app(app)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
app.config.from_object(config['deployConfig'])
csrf.init_app(app)

# Status errors
@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('login')), 401

@app.errorhandler(404)
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

app.register_error_handler(401, status_401)
app.register_error_handler(404, status_404)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.getById(db, id)

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
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


@app.route('/form', methods = ['GET'])
@login_required
def form():
    institution = ModelInstitution.getById(db, current_user.institution_id)
    equipments = ModelEquipment.getAllByInstitutionId(db, institution.id)
    diagnoses = ModelDiagnosis.getAllDiagnosis(db)
    return render_template('/form.html', institution=institution, equipments=equipments, diagnoses=diagnoses)

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_files = request.files.getlist("file[]")
    contours_files = request.files.getlist("contour-files[]")
    institution = ModelInstitution.getById(db, current_user.institution_id)
    operator = current_user.operator_name
    tipoEstudio = request.form['tipo-estudio']
    diagnosis = ModelDiagnosis.getById(db, request.form['tipo-diagnostico'])
    equipo = ModelEquipment.getById(db, request.form['equipo'])
    temp_folder= config['deployConfig'].TEMP_FOLDER
    study_name = uploaded_files[0].filename.split("/")[0]
    if (verify(db, study_name)):
        flash(f"El estudio {study_name} ya fue cargado anteriormente.")
        return redirect(url_for('form'))
    else:
        response = uploadCompleteStudy(institution, operator, tipoEstudio, diagnosis, equipo, uploaded_files, temp_folder, contours_files, study_name)
        if response:
            ModelStudy.uploadStudy(db, study_name, current_user, equipo, diagnosis)
            flash(f"Estudio {study_name} subido correctamente.")
            return redirect(url_for('form'))
        else:
            flash("Error al subir el estudio. Intente nuevamente.")
            return redirect(url_for('form'))


# main
if __name__ == '__main__':
    app.run()