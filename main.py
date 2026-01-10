import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-123') # Best practice: use env var

# 1. DATABASE CONFIGURATION
# Matches the service name 'db' we will use in docker-compose.yml
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'sqlite:///todo.db' # Local fallback for development
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. MODELS (Tables)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create tables automatically if they don't exist
with app.app_context():
    db.create_all()

# 3. ROUTES
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"])
        new_user = User(username=request.form["username"], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit() # Saves to Postgres/SQLite
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("home"))
        return "Login failed"
    return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        # Create new Todo object
        due_date_obj = datetime.strptime(request.form['duedate'], '%Y-%m-%d')
        new_todo = Todo(
            content=request.form['newItem'],
            due_date=due_date_obj,
            user_id=session['user_id']
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))

    # Fetch ONLY the current user's items from the DB
    user_todos = Todo.query.filter_by(user_id=session['user_id']).all()
    
    # Simple Date Logic for the UI
    curr_day = datetime.now().strftime('%d %B %Y, %A')
    return render_template('index.html', list_items=user_todos, today=curr_day, leng=len(user_todos))

@app.route('/delete-item', methods=['POST'])
def delete_item():
    todo_id = request.form['checkbox']
    todo_to_delete = Todo.query.get(todo_id)
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
