from flask import Flask,render_template, request, redirect, session, url_for
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
def index():
    return redirect(url_for("login")) 

@app.route("/img")
def img():
    return render_template("/img.html")
   
@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")
        users = load_users()
        for user in users["users"]:
            if user["email"] == email and bcrypt.checkpw(password, user["password"].encode("utf-8")):
                session["user"]=email
                return redirect(url_for("home"))
            return "¡Credenciales incorrectas! intente nuevamente"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")
        if user_exists(email):
            return "Ñao Ñao, este usuario ya existe. Por favor inicie sesión o regístrese."
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = {"email": email, "password": hashed_password.decode("utf-8")}
        users = load_users()
        users["users"].append(new_user)
        save_users(users)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html") #render renderiza una plantilla html

@app.route("/users")
def users():
    return render_template("users.html") #render renderiza una plantilla html

@app.route("/prueba")
def prueba():
    return render_template("prueba.html")

@app.route("/profile")
def profile():
    if "user" in session:
        user_email = session["user"]
        return render_template("profile.html", user=user_email)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.secret_key = "supersecretkey"
    app.run(debug=True) #Debug es aprueba ed errores