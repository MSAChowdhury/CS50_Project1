import os

from flask import Flask, session, render_template, url_for, request ,logging, redirect,flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bootstrap import Bootstrap
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key="12345678bdProject"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
Bootstrap(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def login():
    return render_template("login.html")
#register_form
@app.route("/register", methods = ['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        address = request.form.get("address")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))
        print(name)
        print(email)
        
        if password == confirm:
            db.execute("INSERT INTO users (username,password,email,address) VALUES (:username, :password, :email, :address)",
            {"username": name, "password": secure_password, "email": email, "address": address})    
            db.commit()
            return render_template("login.html")     
    return render_template("register.html")    

@app.route("/home")
def home():
    return render_template("home.html")    
