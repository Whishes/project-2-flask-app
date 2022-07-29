
from flask import Flask, redirect, render_template, request, session
import gunicorn
import bcrypt
import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL", 'dbname=niceities')
SECRET_KEY = os.environ.get("SECRET_KEY", "niceities-backup")

app = Flask(__name__)
app.secret_key = SECRET_KEY.encode()

@app.route("/", methods=["GET", "POST"])
def index():
    user = None
    if "user" in session:
        user = session.get("user")
        #print(user)
    if request.method == "GET":
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT sentences.user_id, sentences.sentence, sentences.likes, sentences.id, users.username, sentences.liked_by_users
        FROM sentences 
        INNER JOIN users ON sentences.user_id = users.id
        ORDER BY sentences.likes DESC 
        LIMIT 5;
        """)
        top_sentences = cursor.fetchall()
        #print(top_sentences)
        cursor.execute("""
        SELECT sentences.user_id, sentences.sentence, sentences.likes, sentences.id, users.username, sentences.liked_by_users
        FROM sentences 
        INNER JOIN users ON sentences.user_id = users.id
        ORDER BY RANDOM()
        LIMIT 5;
        """)
        random_sentences = cursor.fetchall()
        connection.close()
        #print(user)
        
        return render_template("index.html", user=user, top_sentences = top_sentences, random_sentences = random_sentences)
    if request.method == "POST":
        if "user" not in session:
            return redirect("/")
        submit_type = request.form["submit_type"]
        #print(submit_type)

        if submit_type == "like_button":
            try:
                user_id = int(request.form["user_id"])
                #print(user_id)
                sentence_id = request.form["sentence_id"]
                connection = psycopg2.connect(DATABASE_URL)
                cursor = connection.cursor()
                cursor.execute(f"SELECT likes FROM sentences WHERE id = {sentence_id}")
                sentence_thing = cursor.fetchone()
                print("likes value:",sentence_thing[0])
                cursor.execute(f"UPDATE sentences SET likes = {sentence_thing[0] + 1}, liked_by_users = array_append(liked_by_users, {user_id}) WHERE id = {sentence_id}")
                connection.commit()
                connection.close()
                return redirect("/")
            except:
                return redirect("/")
        elif submit_type == "unlike_button":
            try:
                user_id = int(request.form.get("user_id"))
                sentence_id = request.form.get("sentence_id")
                connection = psycopg2.connect(DATABASE_URL)
                cursor = connection.cursor()
                cursor.execute(f"SELECT likes FROM sentences WHERE id = {sentence_id}")
                sentence_thing = cursor.fetchone()
                print("likes value:", sentence_thing[0])
                cursor.execute(f"UPDATE sentences SET likes = {sentence_thing[0] - 1}, liked_by_users = array_remove(liked_by_users, {user_id}) WHERE id = {sentence_id}")
                connection.commit()
                connection.close()
                return redirect("/")
            except:
                return redirect("/")
        else:
            return redirect("/")

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
            connection.close()
            # if no results do this
            return redirect("/login")
        else:
            #if there is a result do this
            results = cursor.fetchall()
            connection.close()
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
    if "user" not in session:
        return redirect("/")

    user = session.get("user")
    #print(user)
    return render_template("create.html", user=user)

@app.route("/create_action", methods=["POST"])
def create_sentence():
    if "user" not in session:
        return redirect("/")

    # get form data
    user_id = request.form.get("user_id")
    sentence_str = request.form.get("sentence")

    #print("user id: " + user_id)

    # save form data to database
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO sentences (user_id, sentence) VALUES (%s, %s)", (user_id, sentence_str))
    connection.commit()
    connection.close()

    return redirect("/")

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

@app.route("/like_button_action", methods=["POST"])
def like_button_action():
    user_id = int(request.form.get("user_id"))
    sentence_id = request.form.get("sentence_id")
    amnt_of_likes = int(request.form.get("sentence_likes"))
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE sentences SET likes = {amnt_of_likes + 1}, liked_by_users = array_append(liked_by_users, {user_id}) WHERE id = {sentence_id}")
    connection.commit()
    connection.close()
    return redirect("/")

@app.route("/unlike_button_action", methods=["POST"])
def unlike_button_action():
    user_id = int(request.form.get("user_id"))
    sentence_id = request.form.get("sentence_id")
    amnt_of_likes = int(request.form.get("sentence_likes"))
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE sentences SET likes = {amnt_of_likes - 1}, liked_by_users = array_remove(liked_by_users, {user_id}) WHERE id = {sentence_id}")
    connection.commit()
    connection.close()
    return redirect("/")

@app.route("/shared/<sentence_id>")
def share_Sentence(sentence_id):
    user = None
    if "user" in session:
        user = session.get("user")
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f"""SELECT sentences.user_id, sentences.sentence, sentences.likes, sentences.id, users.username, sentences.liked_by_users
        FROM sentences 
        INNER JOIN users ON sentences.user_id = users.id
        WHERE sentences.id = {sentence_id}""")
    returned_sentence = cursor.fetchone()
    connection.close()

    #print(returned_sentence)
    return render_template("share.html", sentence_str = returned_sentence, user=user)

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/")
    user = session.get("user")
    user_id = user["user_id"]
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM sentences WHERE user_id = {user_id};")
    returned_sentences = cursor.fetchall()
    connection.close()
    
    print(returned_sentences)
    return render_template("profile.html", returned_sentences = returned_sentences, user=user)

if __name__ == "__main__":
    app.run(debug=True)
