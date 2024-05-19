from flask import *
from flask_session import *
from pathlib import Path
from datetime import timedelta
from functools import wraps
import hashlib
from flask_mail import Mail
import socket
import os
import requests

path = str(Path(__file__).parent) + "/"

app = Flask("Blog Website")

with open(path+"config.json", "r") as file:
    config = json.load(file)

app.secret_key = config["secret_key"]
app.config['SECRET_KEY'] = config["secret_key"]
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'snehashish.laskar@gmail.com'
app.config['MAIL_PASSWORD'] = 'jioa vavf ifgj opmo'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

host_server=f"http://{str(get_ip())}:8000/"


with open(path+'songs.json', 'r') as file:
    songs = json.load(file)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/dev', methods=['GET', 'POST'])
def dev():
    return render_template("dev.html")

@app.route('/music', methods=['GET', 'POST'])
def music():
    return render_template("music.html", songs=songs)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return "Upcoming Soon!"


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")