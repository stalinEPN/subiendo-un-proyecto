from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import bluetooth as bt
from config import config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required


#Models
from models.ModelUser import ModelUser
from models.ModelDisp import ModelDisp

#entities:
from models.entities.User import User
from models.entities.Disp import Disp

#app design
app = Flask(__name__)
csrf = CSRFProtect()

db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

#methods
def detectarDisp():
    nearby_devices = bt.discover_devices(lookup_names=True)
    dispositivos = []
    id = 1
    for addr, name in nearby_devices:
        dispositivos.append({"id": id, "nombre": name, "mac": addr})
        id += 1
    return dispositivos

def obtenerDisp():
    guardados = ModelDisp.get_disps(db)
    return guardados

def mostrarConectados():
    lista = []
    guardados = obtenerDisp()
    detectados = detectarDisp()
    macs = [diccionario["mac"] for diccionario in detectados]
    i = 1
    for diccionario in guardados:
        estado = "Disponible" if diccionario["dir_mac"] in macs else "Fuera de rango"
        nuevo_diccionario = {
            "id": i,
            "alias": diccionario["alias"],
            "nombre": diccionario["name"],
            "mac": diccionario["dir_mac"],
            "estado": estado
        }
        lista.append(nuevo_diccionario)
        i += 1
    return lista

#routes
@app.route('/')
def index():
    return redirect(url_for('login'))
    #return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        loggedUser = ModelUser.login(db, user)
        if loggedUser != None:
            if loggedUser.password:
                login_user(loggedUser)
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta...")

        else:
            flash("Usuario no encontrado...")
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    return render_template('views/home.html')

@app.route('/View-disps', methods=['GET','POST'])
@login_required
def  viewDisp():
    return render_template('views/viewDisp.html', dispositivos=mostrarConectados())

@app.route('/Admin-disps', methods=['GET','POST'])
@login_required
def  adminDisp():
    return render_template('views/adminDisp.html', guardados=obtenerDisp(), dispositivos=detectarDisp())

@app.route('/agregar', methods=['POST'])
@login_required
def agregarDisp():
    alias = request.form.get('alias')
    name = request.form.get('nombre')
    mac = request.form.get('mac')
    dispos = request.form.get('dispos')

    if mac not in dispos:
        new_disp = Disp(id=None, alias=alias, name=name, mac=mac)    
        ModelDisp.insert_disps(db, new_disp)
    else:
        flash("Este dispositivo ya está registrado.", "error")
    
   
    return redirect(url_for('adminDisp'))

@app.route('/eliminar/<string:mac>')
@login_required
def eliminarDisp(mac):
    ModelDisp.del_disps(db, mac)
    return redirect(url_for('adminDisp'))

@app.route('/About')
@login_required
def about():
    return render_template('views/about.html')


def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return render_template('views/404.html')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    app.run(port=5500)