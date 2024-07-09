from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Pour utiliser flash messages

db = SQLAlchemy(app)

# Modèle de données pour UserProfile
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    class_name = db.Column(db.String(50))
    school = db.Column(db.String(100))
    password = db.Column(db.String(200), nullable=False)
    # Ajoutez d'autres champs selon vos besoins

# Modèle de données pour Project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text)
    deadline = db.Column(db.Date)
    # Ajoutez d'autres champs comme nécessaire

@app.route("/")
def home():
    return render_template('login.html')

def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    
    return render_template('login.html')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

# Route pour le profil utilisateur
@app.route('/profile/')
def profile():
    user_profile = UserProfile.query.filter_by(username='example_user').first()  # Remplacez 'example_user' par votre logique d'authentification
    return render_template('profile.html', user_profile=user_profile)

# Route pour créer un projet
@app.route('/create-project/', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        objectives = request.form['objectives']
        deadline = request.form['deadline']
        # Ajoutez d'autres champs du formulaire
        
        # Créez un nouveau projet
        new_project = Project(title=title, description=description, objectives=objectives, deadline=deadline)
        db.session.add(new_project)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('project_form.html')
