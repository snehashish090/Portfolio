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
import random

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


if not os.path.exists(path+"data"):
    os.mkdir(path+"data")

if not os.path.exists(path+"data/songs.json"):
    with open(path+"data/songs.json", "w") as file:
        json.dump([], file)

if not os.path.exists(path+"data/blogs.json"):
    with open(path+"data/blogs.json", "w") as file:
        json.dump([], file)
        

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
    with open(path+'data/songs.json', 'r') as file:
        songs = json.load(file)
    return render_template("music.html", songs=songs)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    with open(path+'data/blogs.json', 'r') as file:
        blogs = json.load(file)
    return render_template("blog.html", blogs=blogs)

@app.route('/blogPost', methods=['GET', 'POST'])
def blogPost():
    with open(path+'data/blogs.json', 'r') as file:
        blogs = json.load(file)
    if request.method == 'GET':
        uname=config["username"]
        pw=config["password"]
        print(uname,pw)
        return render_template("addBlog.html")
    else:
        var = {
            "id":str(random.randint(100000, 1000000)),
            "title":request.form.get('title'),
            "date":request.form.get('date'),
            "structure":{

            }
        }

        for i in request.form:
            if i!= "title" and i!= "date":
                var["structure"[i]] = request.form.get(i)

        blogs.append(var)

        with open(path+"data/blogs.json", "w") as file:
            json.dump(blogs,file, indent=4)

        return redirect("/blog")
    
@app.route('/deletePost', methods=['GET', 'POST'])
def delPost():
    with open(path+'data/blogs.json', 'r') as file:
        blogs = json.load(file)

    if request.method == 'GET':
        uname=config["username"]
        pw=config["password"]

        print(uname,pw)
        return render_template("deletePost.html", blogs=blogs)
    else:
        id = request.form.get('id')

        for i in blogs:
            if i["id"] == id:
                blogs.remove(i)
                break

        with open(path+"data/blogs.json", "w") as file:
            json.dump(blogs,file, indent=4)

        return redirect("/blog")
if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")