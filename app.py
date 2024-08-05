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

if not os.path.exists(path+"data/projects.json"):
    with open(path+"data/projects.json", "w") as file:
        json.dump([], file)

if not os.path.exists(path+"data/blogs.json"):
    with open(path+"data/blogs.json", "w") as file:
        json.dump([], file)

if not os.path.exists(path+"data/creativity.json"):
    with open(path+"data/creativity.json", "w") as file:
        json.dump([], file)

if not os.path.exists(path+"data/activity.json"):
    with open(path+"data/activity.json", "w") as file:
        json.dump([], file)

if not os.path.exists(path+"data/service.json"):
    with open(path+"data/service.json", "w") as file:
        json.dump([], file)

if not os.path.exists(path+"media"):
    os.mkdir(path+"media")

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


"""

DEVELOPER RELATED

"""
@app.route('/addProject', methods=['GET','POST'])
@login_required
def addProject():
    with open(path+"data/projects.json", "r") as file:
        projects = json.load(file)

    if request.method == 'GET':
        return render_template("addProject.html")
    else:
        data = {
            "id":str(random.randint(100000, 1000000)),
            "title":request.form.get('title'),
            "description":request.form.get('description'),
            "github":request.form.get('github'),
            "image":request.files.get('image'),
        }

        if "url" in request.form:
            data["url"] = request.form.get('url')

        file = data['image']

        if file.filename != "":
            filename = secure_filename(data["id"]+file.filename)
            file.save(os.path.join(path + 'static', filename))

            with open(path+".gitignore", "a") as file:
                file.write("\n"+str(url_for("static", filename=str(filename)))[1:])

            data['image'] = filename

        projects.append(data)

        with open(path+"data/projects.json", "w") as file:
            json.dump(projects, file, indent=4)

        return redirect('/dev')

@app.route('/dev', methods=['GET', 'POST'])
def dev():
    with open(path+'data/projects.json', 'r') as file:
        projects = json.load(file)
    if request.method == 'GET':
        return render_template("dev.html", projects=projects)
    else:
        if "delete" in request.form:
            id = request.form.get('delete-id')
            for i in projects:
                if i['id'] == id:
                    os.remove(os.path.join(path + 'static', i['image']))
                    with open(path+".gitignore","r") as file:
                        lines = file.readlines()
                        with open(path+".gitignore", "w") as file:
                            for line in lines:
                                if i['image'] not in line:
                                    file.write(line)
                    projects.remove(i)
                    with open(path+"data/projects.json", "w") as file:
                        json.dump(projects, file, indent=4)

            with open(path+"data/projects.json", "w") as file:
                json.dump(projects, file, indent=4)
            return redirect('/dev')
        else:
            image = request.files.get("image")
            id = request.form.get("edit-id")

            for project in projects:
                if project['id'] == id:

                    index = projects.index(project)

                    if image.filename != "":
                        filename = secure_filename(id+image.filename)
                        image.save(os.path.join(path +'static', filename))

                        with open(path+".gitignore", "a") as file:
                            file.write("\n"+str(url_for("static", filename=str(filename)))[1:])

                        old_img = project["image"]
                        project["image"] = filename

                        os.remove(path+"static/{}".format(old_img))
                        with open(path+".gitignore","r") as file:
                            lines = file.readlines()
                            with open(path+".gitignore", "w") as file:
                                for line in lines:
                                    if old_img not in line:
                                        file.write(line)

                    project['id'] = request.form.get("edit-id")
                    project['title'] = request.form.get("title")
                    project["description"] = request.form.get("description")

                    if "url" in request.form:
                        project["url"] = request.form.get("url")
                    elif "url" not in request.form and "url" in project:
                        del project["url"]

                    if "github" in request.form:
                        project["github"] = request.form.get("github")
                    elif "github" not in request.form and "github" in project:
                        del project["github"]

                    projects[index] = project

                    with open(path+"data/projects.json", "w") as file:
                        json.dump(projects, file, indent=4)

            return redirect('/dev')

"""

BLOG RELATED

"""

@app.route('/blog/<id>', methods=['GET', 'POST'])
def blogSpecific(id):
    with open(path+'data/blogs.json', 'r') as file:
        blogs = json.load(file)
        blogs.reverse()

    blog = []

    for i in blogs:
        if i["id"] == id:
            blog.append(i)
            break

    if request.method == 'GET':
        return render_template("blog.html", blogs=blog)
    else:

        id = request.form.get('delete-id')

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



@app.route('/blog', methods=["GET"])
def blogRouter():
    with open(path+'data/blogs.json', 'r') as file:
        blogs = json.load(file)
        blogs.reverse()

    return render_template("blog-router.html", blogs=blogs)

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
                    filename = secure_filename(var["id"]+file.filename)
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
@login_required
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
                    filename = secure_filename(var['id']+file.filename)
                    var['structure'][i] = url_for("static", filename=str(filename))
                    file.save(os.path.join(path + 'static', filename))

                    with open(path+".gitignore", "a") as file:
                        file.write("\n"+str(url_for("static", filename=str(filename)))[1:])

        blogs[blogs.index(myblog)] = var

        with open(path + "data/blogs.json", "w") as file:
            json.dump(blogs, file, indent=4)

        return redirect("/blog")

"""

AUTHENTICATION RELATED

"""

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





"""
CREATIVITY PAGE RELATED
"""

@app.route("/creativity", methods=["GET", "POST"])
def creativity():
    with open(path+"data/creativity.json", "r") as file:
        activities = json.load(file)

    if request.method == "GET":
        return render_template("creativity.html", activities=activities)
    else:

        if "edit" not in request.form:
            for activity in activities:
                if activity["id"] == request.form.get("delete-id"):
                    img = activity["image"]

                    os.remove(path+f"static/{img}")
                    with open(path+".gitignore","r") as file:
                        lines = file.readlines()
                        with open(path+".gitignore", "w") as file:
                            for line in lines:
                                if activity['image'] not in line:
                                    file.write(line)

                    activities.remove(activity)
                    with open(path+"data/creativity.json", "w") as file:
                        json.dump(activities, file, indent=4)
        else:
            image = request.files.get("image")
            id = request.form.get("edit-id")

            for activity in activities:
                print(activity['id'], id)
                if activity['id'] == id:


                    index = activities.index(activity)

                    if image.filename != "":
                        filename = secure_filename(id+image.filename)
                        image.save(os.path.join(path +'static', filename))

                        with open(path+".gitignore", "a") as file:
                            file.write("\n"+str(url_for("static", filename=str(filename)))[1:])

                        old_img = activity["image"]
                        activity["image"] = filename

                        os.remove(path+"static/{}".format(old_img))
                        with open(path+".gitignore","r") as file:
                            lines = file.readlines()
                            with open(path+".gitignore", "w") as file:
                                for line in lines:
                                    if old_img not in line:
                                        file.write(line)

                    activity["title"] = request.form.get("title")
                    activity["description"] = request.form.get("description")
                    activity["long-description"] = request.form.get("long-description")

                    activities[index] = activity

                    if request.form.get('type').lower() != str(request.path)[1:]:
                        with open(path+f"data/{request.form.get('type').lower()}.json", "r") as file2:
                            exisiting = json.load(file2)
                            exisiting.append(activity)
                            with open(path+f"data/{request.form.get('type').lower()}.json", "w") as file:
                                json.dump(exisiting, file, indent=4)

                        activities.remove(activity)
                        with open(path+f"data/{str(request.path)[1:]}.json", "w") as file:
                            json.dump(activities, file, indent=4)
                    else:
                        with open(path+f"data/{str(request.path)[1:]}.json", "w") as file:
                            json.dump(activities, file, indent=4)

    return redirect('/creativity')


"""

SERVICE PAGE RELATED


"""
@app.route("/service", methods=["GET", "POST"])
def service():
    with open(path+"data/service.json", "r") as file:
        activities = json.load(file)

    if request.method == "GET":
        return render_template("service.html", activities=activities)
    else:

        if "edit" not in request.form:
            for activity in activities:
                if activity["id"] == request.form.get("delete-id"):
                    img = activity["image"]

                    os.remove(path+f"static/{img}")
                    with open(path+".gitignore","r") as file:
                        lines = file.readlines()
                        with open(path+".gitignore", "w") as file:
                            for line in lines:
                                if activity['image'] not in line:
                                    file.write(line)

                    activities.remove(activity)
                    with open(path+"data/service.json", "w") as file:
                        json.dump(activities, file, indent=4)
        else:
            image = request.files.get("image")
            id = request.form.get("edit-id")

            for activity in activities:
                print(activity['id'], id)
                if activity['id'] == id:


                    index = activities.index(activity)

                    if image.filename != "":
                        filename = secure_filename(id+image.filename)
                        image.save(os.path.join(path +'static', filename))

                        with open(path+".gitignore", "a") as file:
                            file.write("\n"+str(url_for("static", filename=str(filename)))[1:])

                        old_img = activity["image"]
                        activity["image"] = filename

                        os.remove(path+"static/{}".format(old_img))
                        with open(path+".gitignore","r") as file:
                            lines = file.readlines()
                            with open(path+".gitignore", "w") as file:
                                for line in lines:
                                    if old_img not in line:
                                        file.write(line)

                    activity["title"] = request.form.get("title")
                    activity["description"] = request.form.get("description")
                    activity["long-description"] = request.form.get("long-description")

                    activities[index] = activity

                    if request.form.get('type').lower() != str(request.path)[1:]:
                        with open(path+f"data/{request.form.get('type').lower()}.json", "r") as file2:
                            exisiting = json.load(file2)
                            exisiting.append(activity)
                            with open(path+f"data/{request.form.get('type').lower()}.json", "w") as file:
                                json.dump(exisiting, file, indent=4)

                        activities.remove(activity)
                        with open(path+f"data/{str(request.path)[1:]}.json", "w") as file:
                            json.dump(activities, file, indent=4)
                    else:
                        with open(path+f"data/{str(request.path)[1:]}.json", "w") as file:
                            json.dump(activities, file, indent=4)
    return redirect('/service')


"""

ACTIVITY PAGE RELATED

"""
@app.route("/activity", methods=["GET", "POST"])
def activity():
    with open(path+"data/activity.json", "r") as file:
        activities = json.load(file)

    if request.method == "GET":
        return render_template("activity.html", activities=activities)
    else:

        if "edit" not in request.form:
            for activity in activities:
                if activity["id"] == request.form.get("delete-id"):
                    img = activity["image"]

                    os.remove(path+f"static/{img}")
                    with open(path+".gitignore","r") as file:
                        lines = file.readlines()
                        with open(path+".gitignore", "w") as file:
                            for line in lines:
                                if activity['image'] not in line:
                                    file.write(line)

                    activities.remove(activity)
                    with open(path+"data/activity.json", "w") as file:
                        json.dump(activities, file, indent=4)
        else:
            image = request.files.get("image")
            id = request.form.get("edit-id")

            for activity in activities:
                print(activity['id'], id)
                if activity['id'] == id:


                    index = activities.index(activity)

                    if image.filename != "":
                        filename = secure_filename(id+image.filename) + id
                        image.save(os.path.join(path +'static', filename))

                        with open(path+".gitignore", "a") as file:
                            file.write("\n"+str(url_for("static", filename=str(filename)))[1:])

                        old_img = activity["image"]
                        activity["image"] = filename

                        os.remove(path+"static/{}".format(old_img))
                        with open(path+".gitignore","r") as file:
                            lines = file.readlines()
                            with open(path+".gitignore", "w") as file:
                                for line in lines:
                                    if old_img not in line:
                                        file.write(line)

                    activity["title"] = request.form.get("title")
                    activity["description"] = request.form.get("description")
                    activity["long-description"] = request.form.get("long-description")

                    activities[index] = activity

                    if request.form.get('type').lower() != str(request.path)[1:]:
                        with open(path+f"data/{request.form.get('type').lower()}.json", "r") as file2:
                            exisiting = json.load(file2)
                            exisiting.append(activity)
                            with open(path+f"data/{request.form.get('type').lower()}.json", "w") as file:
                                json.dump(exisiting, file, indent=4)

                        activities.remove(activity)
                        with open(path+f"data/{str(request.path)[1:]}.json", "w") as file:
                            json.dump(activities, file, indent=4)
                    else:
                        with open(path+f"data/{str(request.path)[1:]}.json", "w") as file:
                            json.dump(activities, file, indent=4)
    return redirect('/activity')

@app.route("/addActivity", methods=["POST","GET", "DELETE"])
@login_required

def addActivity():
    with open(path+"data/creativity.json", "r") as file:
        creativity = json.load(file)
    with open(path+"data/activity.json", "r") as file:
        activity= json.load(file)
    with open(path+"data/service.json", "r") as file:
        service = json.load(file)

    if request.method == "GET":
        return render_template("addActivity.html")
    else:

        mode = request.form.get('type').lower()
        data = {
            "id":str(random.randint(100000, 1000000)),
            "title":request.form.get('title'),
            "image":request.files.get("image"),
            "description":request.form.get("description"),
            "long-description":request.form.get('long-description')
        }

        file = data['image']

        if file.filename != "":
            filename = secure_filename(data["id"]+file.filename)
            file.save(os.path.join(path + 'static', filename))

            with open(path+".gitignore", "a") as file:
                file.write("\n"+str(url_for("static", filename=str(filename)))[1:])

            data['image'] = filename

        if mode == "creativity":
            with open(path+"data/creativity.json", "w") as file:
                creativity.append(data)
                json.dump(creativity, file, indent=4)

        elif mode == "activity":
            with open(path+"data/activity.json", "w") as file:
                activity.append(data)
                json.dump(activity, file, indent=4)

        elif mode == "service":
            with open(path+"data/service.json", "w") as file:
                service.append(data)
                json.dump(service, file, indent=4)

        return redirect('/')






"""

RELTAED TO MUSIC PAGE

"""


@app.route('/music', methods=['GET', 'POST'])
def music():
    with open(path+'data/songs.json', 'r') as file:
        songs = json.load(file)
    if request.method == 'GET':
        return render_template("music.html", songs=songs)
    else:
        index = int(request.form.get('delete-id'))
        del songs[index]
        with open(path+'data/songs.json', 'w') as file:
            json.dump(songs, file)

        return redirect('/music')


@app.route("/addSong", methods=["POST","GET", "DELETE"])
@login_required
def addSong():
    with open(path+"data/songs.json", "r") as file:
        songs = json.load(file)

    if request.method == "GET":
        return render_template("addSong.html")
    else:
        data = {
            "url":request.form.get("url"),
            "image":request.form.get("image"),
            "title":request.form.get('title')
        }

        songs = [data]+songs
        with open(path+"data/songs.json", "w") as file:
            json.dump(songs, file, indent=4)

        return redirect('/music')


"""

RELTAED TO PUBLIC FILE ARCHIVE FEATURE

"""

@app.route('/files/<path:filename>')
def download_file(filename):
    return send_from_directory(path+"media", filename)

@app.route("/files")
def file_explorer():
    files = os.listdir(path+"media")
    return render_template("media.html", files=files)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        filename = file.filename
        file.save(os.path.join(path+"media", filename))
        return redirect(url_for('index'))

@app.route('/admin/upload', methods=["GET", "POST"])
@login_required
def upload_file_admin():
    return render_template("mediaUpload.html")

# Route to delete a file from the file archive
@app.route('/delete/<filename>', methods=['GET'])
@login_required
def delete_file(filename):
    try:
        os.remove(path+"media"+"/"+filename)
        return redirect("/files")
    except OSError as e:
        return f'Error deleting file {filename}: {e}'


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
