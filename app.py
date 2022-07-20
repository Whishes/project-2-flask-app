
from flask import Flask, render_template
import gunicorn
import bcrypt
import psycopg2

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
    