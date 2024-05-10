from flask import Flask,render_template, request, redirect, session
import json
import os
import bcrypt

app = Flask(__name__)

db_file_path = os.path.join(os.path.dirname(__file__), "data/users.json")

def load_users():
    with open(db_file_path, "r") as f:
        return json.load(f)

def save_users(users):
    with open(db_file_path, "w") as f:
        json.dump(users, f, indent=4)

def user_exists(email):
    users = load_users()
    for user in users["users"]:
        if user["email"]==email:
            return True
    return False
    
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html") #render renderiza una plantilla html

@app.route("/users")
def users():
    return render_template("users.html") #render renderiza una plantilla html

@app.route("/prueba")
def prueba():
    return render_template("prueba.html")




if __name__ == "__main__":
    app.run(debug=True) #Debug es aprueba ed errores