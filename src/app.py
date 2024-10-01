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
        flash("incorrect username or password")
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.id
            print(f"User: {username} logging in with password: {password}")
            return redirect(url_for("home"))
        else:
            flash("incorrect username or password")
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

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

    return redirect("/")


@app.route("/home")
def home():
    # add link/ button to the search thing
    sql = text("""
        SELECT Posts.id, Posts.content, Posts.creation_time, Users.username, COUNT(Likes.id) as likes
        FROM Posts
        LEFT JOIN Users
        ON Posts.user_id = Users.id
        LEFT JOIN Likes
        ON Posts.id = Likes.post_id
        GROUP BY Posts.id, Users.id
        ORDER BY Posts.id DESC
    """)
    result = db.session.execute(sql)
    posts = result.fetchall()
    print(posts)
    return render_template("home.html", posts=posts)

@app.route("/likes/<int:post>", methods=["POST"])
def like(post):
    sql = text("""
        INSERT INTO Likes (post_id, liker_id)
        VALUES(:post_id, :user_id)
        ON CONFLICT DO NOTHING
        RETURNING TRUE
    """)
    db.session.execute(sql, {"post_id":post, "user_id":session["user_id"]})
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/new_post")
def new_post():
    return render_template("send_new_post.html")

@app.route("/send", methods=["POST"])
def add_posts():
    content = request.form["content"]
    sql = text("""
        INSERT INTO posts (content, user_id) 
        VALUES (:content, :user_id)
        RETURNING TRUE
    """)
    result = db.session.execute(sql, {"content":content, "user_id":session["user_id"]})
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
