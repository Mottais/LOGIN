from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Configuration de la connexion MySQL
db = MySQLdb.connect(host="localhost", user="toto", passwd="toto", db="charpente_db")
cursor = db.cursor()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Utilisateur(UserMixin):
    def __init__(self, id, nom, email, mot_de_passe):
        self.id = id
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe


@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT id, nom, email, mot_de_passe FROM utilisateur WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return Utilisateur(user[0], user[1], user[2], user[3])
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')
        hashed_password = generate_password_hash(mot_de_passe)

        try:
            cursor.execute("INSERT INTO utilisateur (nom, email, mot_de_passe) VALUES (%s, %s, %s)",
                           (nom, email, hashed_password))
            db.commit()
            flash('Registration successful!', category='success')
            return redirect(url_for('login'))
        except MySQLdb.Error as e:
            db.rollback()
            flash(f'Error: {e}', category='error')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')

        cursor.execute("SELECT id, nom, email, mot_de_passe FROM utilisateur WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], mot_de_passe):
            login_user(Utilisateur(user[0], user[1], user[2], user[3]), remember=True)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your credentials.', category='error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.nom)

if __name__ == '__main__':
    app.run(debug=True)
