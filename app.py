import requests
from functools import wraps
from werkzeug.utils import secure_filename
from libs.functions import uploadFileTime, generateFileName, determineFileType, groupFileData
from libs.validateforms import SignupForm, LoginForm, UploadFile
from libs.firebase import signUp, logIn, userDataStorage, getUserData, userFileStorage, userAddFileHistory, getFileURL
from flask import Flask, render_template, request, flash, url_for, redirect, session, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'anotherkey098765'

brand = ' · RS Report'


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return f(*args, **kwargs)
        else:
            flash('Sin autorización. Por favor inicia sesión', 'danger')
            return redirect(url_for('login'))

    return wrap




# ANCHOR Home

@app.route('/')
def home():
    title = 'Inicio' + brand
    return render_template('home.html', title=title)




# ANCHOR User Sign Up

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title = 'Signup' + brand

    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate():

        userData = {
            'name': (form.userName.data).capitalize(),
            'lastname': (form.userLastname.data).capitalize(),
            'email': form.emailSign.data,
            'password': form.passwordSign.data
        }

        if signUp(userData['email'], userData['password']) and userDataStorage(userData):

            flash('Ahora te encuentras registrado. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))

        else:
            flash('La cuenta ya existe con el correo que acabas de ingresar. Intenta nuevamente.', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html', title=title, form=form)




# ANCHOR User Log In

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login' + brand

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.emailLog.data
        password = form.passwordLog.data

        if logIn(email, password):

            session['logged'] = True
            session['userkey'], data = getUserData(email)

            session['user'] = data['name'] + ' ' + data['lastname']
            session['email'] = data['email']

            msg = 'Ahora puedes crear nuevos reportes y descargarlos'
            return render_template('home.html', msg=msg)

        else:
            flash('Error iniciando sesión, el correo o la contraseña no coinciden', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', title=title, form=form)




# ANCHOR User Log Out

@app.route('/logout')
def logout():
    session.clear()
    info = 'Has cerrado la sesión'
    return render_template('home.html', info=info)



# ANCHOR File Upload

@app.route('/fileupload', methods=['GET', 'POST'])
@is_logged_in
def fileupload():
    title = 'Subir Archivo' + brand

    form = UploadFile()

    if form.validate_on_submit():

        origin = 'user'
        
        f = form.userFile.data
        filename = secure_filename(f.filename)

        if userFileStorage(session['userkey'], filename, f):

            filetype = determineFileType(filename)
            date, time = uploadFileTime()
            url = getFileURL(session['userkey'], filename)

            session['filedata'] = groupFileData(filename, filetype, origin, date, time, url)

            if userAddFileHistory(session['userkey'], session['filedata']):
                flash('El archivo ahora se encuentra en la base de datos', 'success')
                return redirect(url_for('filemanager'))
            
            else:
                flash('Ha ocurrido un error mientras se cargaba el archivo en la base de datos. Intenta de nuevo', 'danger')
                return redirect(url_for('fileupload'))

        else:
            flash('Ha ocurrido un error mientras se cargaba el archivo en la base de datos. Intenta de nuevo', 'danger')
            return redirect(url_for('fileupload'))


    elif 'channelID' in request.form:

        origin = 'cloud'

        channelID = request.form['channelID']

        cloudurl = 'https://api.thingspeak.com/channels/'+channelID+'/feeds.csv'
        f = requests.get(cloudurl)

        if f.ok == True:

            filename = generateFileName(channelID)
            filetype = determineFileType(filename)

            userFileStorage(session['userkey'], filename, f)

            date, time = uploadFileTime()
            url = getFileURL(session['userkey'], filename)

            session['filedata'] = groupFileData(filename, filetype, origin, date, time, url)

            if userAddFileHistory(session['userkey'], session['filedata']):
                flash('El archivo ahora se encuentra en la base de datos', 'success')
                return redirect(url_for('filemanager'))
            
            else:
                flash('Ha ocurrido un error mientras se cargaba el archivo en la base de datos. Intenta de nuevo', 'danger')
                return redirect(url_for('fileupload'))

        else:
            flash('El número del Channel ID que escribió no existe o es incorrecto. Pruebe escribiendo otro número.', 'danger')
            return redirect(url_for('fileupload'))

    return render_template('fileupload.html', title=title, form=form)




@app.route('/filemanager')
@is_logged_in
def filemanager():
    title = 'Características del Archivo' + brand

    return render_template('filemanager.html', title=title)




@app.route('/reportform')
@is_logged_in
def report():
    title = 'Creación del Reporte' + brand
    return render_template('reportform.html', title=title)




@app.route('/dashboard')
@is_logged_in
def dashboard():
    title = 'Dashboard' + brand
    return render_template('dashboard.html', title=title)




@app.route('/about')
def about():
    title = 'Nosotros' + brand
    return render_template('about.html', title=title)




@app.route('/docs')
def docs():
    title = 'Documentación' + brand
    return render_template('docs.html', title=title)





if __name__ == "__main__":
    app.run(debug=True)