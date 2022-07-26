
from distutils.log import error
from flask import Flask, redirect, render_template, request, session
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
    user = None
    if "user" in session:
        user = session.get("user")
        #print(user)
    return render_template("index.html", user=user)

@app.route("/login")
def login():
    if "user" in session:
        return redirect("/")
    return render_template("login.html")  

@app.route("/login_action", methods=["POST"])
def doLogin():
    if "user" not in session:
        #check hashed password
        def check(string, hashed_string):
            return bcrypt.checkpw(string.encode(), hashed_string.encode())
        # get user login data from login form
        username = str(request.form.get("username"))
        password = request.form.get("password")

        # connect/execute command to check DB for username
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, email, hashed_password FROM users WHERE username = %s", [username])

        if cursor.rowcount == 0:
            # if no results do this
            return redirect("/login")
        else:
            #if there is a result do this
            results = cursor.fetchall()
            #print(results)
            # checks password hash to make sure it matches
            if (check(password, results[0][3])):
                user_data = {"user_id": results[0][0], "username": results[0][1],"email": results[0][2]}
                #print(user_data)
                # put all non-sensitive user data into session for later
                session["user"] = user_data
                return redirect("/")
            else:
                return redirect("/login")
    return redirect("/")

@app.route("/signout_action")
def signout_action():
    if "user" in session:
        session.pop("user")
    return redirect("/")

@app.route("/create")
def create():
    user = None
    if "user" not in session:
        return redirect("/")

    user = session.get("user")
    return render_template("create.html", user=user)

@app.route("/register")
def regiser():
    if "user" in session:
        return redirect("/")
    return render_template("register.html") 


@app.route("/register_action", methods=["POST"])
def register_action():
    if "user" in session:
        return redirect("/")
    # get form data
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    # hash password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # save user to the DB
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)", (username, email, password_hash))
    connection.commit()
    connection.close()

    return redirect("/login")
    
if __name__ == "__main__":
    app.run(debug=False)
    

