from flask import Flask
from flask import redirect, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
# csrf vulnerability

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

@app.route("/", methods=["GET"]) 
def loginpage():
    return render_template("loginpage.html", title="login") 

@app.route("/", methods=["POST"])
def handlelogin():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("""
        SELECT id, password
        FROM Users
        WHERE username = :username
    """)
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        pass #add check
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            pass# both correct, flash?
        else:
            pass # incorrect password
    print(f"User: {username} logging in with password: {password}")
    # session["username"] = username -> plus add the checks!
    return redirect(url_for("home"))

@app.route("/register")
def registerpage():
    return render_template("registerpage.html")

@app.route("/register", methods=["POST"])
def handleregister():
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if confirm_password != password:
        flash("the passwords do not match! please try again")
        return redirect("/register")
    
    hash_value = generate_password_hash(password)
    sql = text("""
        INSERT INTO Users (username, password)
        VALUES (:username, :password)
    """)
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

    flash("the registeration has been succesful!")
    return redirect("/")


@app.route("/home")
def home():
    # add link/ button to the search thing
    sql = text("""
        SELECT id, content, user_id, likes, creation_time
        FROM Posts
        ORDER BY id DESC
    """)
    result = db.session.execute(sql)
    posts = result.fetchall()
    return render_template("home.html", posts=posts)
    

@app.route("/new_post")
def new_post():
    return render_template("send_new_post.html")

@app.route("/send", methods=["POST"])
def add_posts():
    content = request.form["content"]
    sql = text("""
        INSERT INTO posts (content) 
        VALUES (:content)
        RETURNING TRUE
    """)
    result = db.session.execute(sql, {"content":content})
    success = result.fetchone() or False
    if success:
        db.session.commit()

    return redirect(url_for("home"))

@app.route("/profile")
def profile():
    # does the user have a premission to view the profile?
    return render_template("profile.html")

@app.route("/search") # no need to add get? -> might just add anyway
def search():
    pass
# add searchbar, can search by user or by word in post/song or smth
# possibility to log out (mainpage, or profile?)
