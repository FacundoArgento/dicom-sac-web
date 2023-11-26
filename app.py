from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_simple_captcha import CAPTCHA
from datetime import datetime
from os import listdir

# Config
from config import config
from models.ModelStudy import ModelStudy

# Models
from models.ModelUser import ModelUser
from models.ModelInstitution import ModelInstitution
from models.ModelEquipment import ModelEquipment
from models.ModelDiagnosis import ModelDiagnosis

# Entities
from models.entities.User import User

# Payload
from services.DicomUploader import uploadCompleteStudy, save_tmp_folders, remove_tmp_folders

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] =  512 * 1024 * 1024 # 500 MB
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
    if listdir(config['deployConfig'].TEMP_FOLDER): 
            print("borrando archivos...")
            remove_tmp_folders(config['deployConfig'].TEMP_FOLDER)
    return render_template('/form.html', institution=institution, equipments=equipments, diagnoses=diagnoses)

@app.route("/upload", methods=["POST"])
def upload():
    contour_file = request.files['contour-file']
    institution = ModelInstitution.getById(db, current_user.institution_id)
    operator = current_user.operator_name
    tipoEstudio = request.form['tipo-estudio']
    diagnosis = ModelDiagnosis.getById(db, request.form['tipo-diagnostico'])
    equipo = ModelEquipment.getById(db, request.form['equipo'])
    temp_folder= config['deployConfig'].TEMP_FOLDER
    study_name = "{0}-{1} {2}-{3}-{date:%Y-%m-%d_%H:%M:%S}".format(institution.name, equipo.model, equipo.potency, diagnosis.name, date=datetime.now())
    response = uploadCompleteStudy(institution, operator, tipoEstudio, diagnosis, equipo, temp_folder, contour_file, study_name)
    if response:
        ModelStudy.uploadStudy(db, study_name, current_user, equipo, diagnosis)
        flash(f"Estudio subido correctamente. Nombre indicado: {study_name}")
        return redirect(url_for('form'))
    else:
        flash("Error al subir el estudio. Intente nuevamente.")
        return redirect(url_for('form'))

@app.route("/save-tmp-files", methods=["POST"])
def save_tmp():
    try:
        temp_folder = config['deployConfig'].TEMP_FOLDER
        if listdir(temp_folder): 
            print("borrando archivos previos...")
            remove_tmp_folders(config['deployConfig'].TEMP_FOLDER)
        if 'files[]' not in request.files:
            return jsonify({'error': 'No se proporcionaron archivos'}), 400
        files = request.files.getlist("files[]")
        save_tmp_folders(files, temp_folder)
        return jsonify({'message': 'Archivo guardado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# main
if __name__ == '__main__':
    app.run()