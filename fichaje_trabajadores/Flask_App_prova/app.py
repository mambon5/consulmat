from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

# Inicializar la aplicación Flask
app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Configuración de la conexión a MySQL
app.config['MYSQL_USER'] = 'root'  # tu usuario de MySQL
app.config['MYSQL_PASSWORD'] = 'Dinamarca24+'  # tu contraseña de MySQL
app.config['MYSQL_DB'] = 'database'  # tu base de datos
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirige al login si no está autenticado

# Crear una clase Usuario (User)
class User(UserMixin):
    def __init__(self, id, tipus_usuari):
        self.id = id
        self.tipus_usuari = tipus_usuari

# Cargar el usuario a partir del id
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuaris WHERE id = %s', (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(user_data['id'], user_data['tipus_usuari'])
    return None

# Ruta principal (Home)
@app.route('/')
@login_required
def home():
    return f'Bienvenido {current_user.id}'

# Ruta de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuaris WHERE correu = %s', (username,))
        user_data = cursor.fetchone()
        
        if user_data and check_password_hash(user_data['contrasenya'], password):  # Compara contraseñas
            user = User(user_data['id'], user_data['tipus_usuari'])
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
