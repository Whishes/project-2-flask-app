
from flask import Flask, render_template
import gunicorn
import bcrypt
import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL", 'dbname=niceities')
SECRET_KEY = os.environ.get("SECRET_KEY", "niceities-backup")

app = Flask(__name__)
app.secret_key = SECRET_KEY.encode()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")   

@app.route("/register")
def regiser():
    return render_template("register.html") 

@app.route("/create")
def create():
    return render_template("create.html")   
    
if __name__ == "__main__":
    app.run(debug=True)
    