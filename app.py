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
import json
from werkzeug.utils import secure_filename
path = str(Path(__file__).parent) + "/"

app = Flask("Blog Website")

with open(path+"config.json", "r") as file:
    config = json.load(file)

app.secret_key = config["secret_key"]
app.config['SECRET_KEY'] = config["secret_key"]
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

mail = Mail(app)
Session(app)

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
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get("logStatus"):
            session["logStatus"] = False
        if session["logStatus"] == False:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrap

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
@login_required
def blogPost():
    if request.method == 'GET':
        return render_template("addBlog.html")
    else:
        with open(path + 'data/blogs.json', 'r') as file:
            blogs = json.load(file)
        
        var = {
            "id": str(random.randint(100000, 1000000)),
            "title": request.form.get('title'),
            "date": request.form.get('date'),
            "structure": {}
        }

        print(dict(request.form), dict(request.files))
        
        for i in request.form:
            if i!= "title" and i!= "date" and "image" not in i:
                var["structure"][i] = request.form.get(i)
            if "image" in i:
                print("Hello Debug?")
                file = request.files.get(i)
                print(file.filename)
                if file.filename == '':
                    continue
                if file:
                    filename = secure_filename(file.filename)
                    var['structure'][i] = url_for("static", filename=str(filename))
                    file.save(os.path.join(path + 'static', filename))

                    with open(path+".gitignore", "a") as file:
                        file.write("\n"+str(url_for("static", filename=str(filename)))[1:])
        
        blogs.append(var)
        print(var)
        with open(path + "data/blogs.json", "w") as file:
            json.dump(blogs, file, indent=4)
        
        return redirect("/blog")

@app.route("/editPost/<post_id>", methods=["GET", "POST"])
def editPost(post_id):
    with open(path+'data/blogs.json', 'r') as file:
        blogs = json.load(file)

    for blog in blogs:
        if blog["id"] == post_id:
            myblog = blog

    print(myblog)

    if request.method == 'GET':
        return render_template("editBlog.html", blog=myblog)
    else:
        var = {
            "id": blog["id"],
            "title": request.form.get('title'),
            "date": request.form.get('date'),
            "structure": {}
        }

        for i in request.form:
            if i!= "title" and i!= "date" and "image" not in i:
                var["structure"][i] = request.form.get(i)
            if "image" in i:
                file = request.files.get(i)
                print(file.filename)
                if file.filename == '':
                    if blog['structure'].get(i) is not None:
                        var['structure'][i] = blog['structure'].get(i)
                    else:
                        continue
                if file:
                    filename = secure_filename(file.filename)
                    var['structure'][i] = url_for("static", filename=str(filename))
                    file.save(os.path.join(path + 'static', filename))

                    with open(path+".gitignore", "a") as file:
                        file.write("\n"+str(url_for("static", filename=str(filename)))[1:])
                        
        blogs[blogs.index(myblog)] = var

        with open(path + "data/blogs.json", "w") as file:
            json.dump(blogs, file, indent=4)
        
        return redirect("/blog")



@app.route('/deletePost', methods=['GET', 'POST'])
@login_required
def delPost():
    with open(path+'data/blogs.json', 'r') as file:
        blogs = json.load(file)

    if request.method == 'GET':
        return render_template("deletePost.html", blogs=blogs)
    else:
        id = request.form.get('id')

        for i in blogs:
            if i["id"] == id:
                for j in i["structure"]:
                    if "image" in j:
                        os.remove(path[:-1]+i["structure"][j])
                    with open(path+".gitignore","r") as file:
                        lines = file.readlines()
                        with open(path+".gitignore", "w") as file:
                            for line in lines:
                                if i["structure"][j][1:] not in line:
                                    file.write(line)
                blogs.remove(i)
                break
            
        with open(path+"data/blogs.json", "w") as file:
            json.dump(blogs,file, indent=4)

        return redirect("/blog")
    

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

    if email == config["email"] and password == config["password"]:
            session["logStatus"] = True
            return redirect("/")
    else:
        return render_template("login.html", error="Invalid Email or Password")
    
@app.route("/logout", methods=["GET", "POST"])
def logout_page():
    session["logStatus"] = False
    return redirect("/")

@app.route("/creativity", methods=["GET", "POST"])
def creativity():
    return render_template("creativity.html")

@app.route("/activity", methods=["GET", "POST"])
def activity():
    return render_template("activity.html")

@app.route("/service", methods=["GET", "POST"])
def service():
    return render_template("service.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")