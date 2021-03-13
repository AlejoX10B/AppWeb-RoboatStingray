import time
import calendar
import pyrebase
from werkzeug.utils import secure_filename

firebaseConfig = {
    'apiKey': "AIzaSyCePI5JkqUiG0ILwG6A45f_xctb77lznk8",
    'authDomain': "rs-report-generator.firebaseapp.com",
    'databaseURL': "https://rs-report-generator-default-rtdb.firebaseio.com",
    'projectId': "rs-report-generator",
    'storageBucket': "rs-report-generator.appspot.com",
    'messagingSenderId': "335249771303",
    'appId': "1:335249771303:web:49f88f1475be8e5b677702"
}

firebase = pyrebase.initialize_app(firebaseConfig)




def signUp(email, password):
    """Creación de usuario en Firebase Auth"""

    auth = firebase.auth()

    try:
        auth.create_user_with_email_and_password(email, password)
    except:
        return False

    return True




def logIn(email, password):
    """Inicio de sesión de usuario en Firebase Auth"""

    auth = firebase.auth()

    try:
        auth.sign_in_with_email_and_password(email, password)
    except:
        return False
    
    return True



def userDataStorage(data):
    """Crea un nuevo registro en la base de datos, almacenando los datos ingresados en el registro."""

    db = firebase.database()

    user = secure_filename(data['name']+data['lastname'])+str(calendar.timegm(time.gmtime()))

    try:
        db.child('users').child(user).set(data)
    except:
       return False

    return True




def getUserData(email):
    """ Obtiene los datos del Usuario """

    db = firebase.database()
    users = db.child('users').order_by_child('email').equal_to(email).get()

    for user in users.each():

        if user.val()['email'] == email:
            return user.key(), user.val()
            
        else:
            return None, None




def userFileStorage(userkey, filename, f):
    """Almacenamiento de los archivos del usuario en Firebase"""

    storage = firebase.storage()

    try:
        storage.child('uploadedFiles/' + userkey + '/' + filename).put(f)
    except:
        return False

    return True




def getFileURL(userkey, filename):
    storage = firebase.storage()

    try:
        url = storage.child('uploadedFiles/' + userkey + '/' + filename).get_url(None)
    except:
        return None
    
    return url




def userAddFileHistory(userkey, filedata):

    db = firebase.database()

    try:
        db.child('users').child(userkey).child('UploadedFiles').push(filedata)
    except:
        return False
    
    return True