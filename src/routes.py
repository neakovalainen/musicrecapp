import secrets
import functools
from flask import redirect, render_template, request, session, url_for, flash, abort
from werkzeug.security import check_password_hash, generate_password_hash
import sql_queries
from app import app

def authenticate(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("loginpage"))
        return f(*args, **kwargs)
    return wrapper


# logging in, out and registration

@app.route("/", methods=["GET"])
def loginpage():
    if "user_id" in session:
        return redirect(url_for("home"))
    return render_template("loginpage.html", title="login")

@app.route("/", methods=["POST"])
def handlelogin():
    if "user_id" in session:
        return abort(403)
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    if not username or not password:
        flash("no username or password given")
        return redirect(url_for("loginpage"))
    user = sql_queries.get_username(username)
    if not user:
        flash("incorrect username or password")
        return redirect(url_for("loginpage"))
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["user_id"] = user.id
        session["csrf_token"] = secrets.token_hex(16)
        return redirect(url_for("home"))
    flash("incorrect username or password")
    return redirect(url_for("loginpage"))

@app.route("/logout")
@authenticate
def logout():
    for item in list(session):
        session.pop(item, None)
    return redirect(url_for("loginpage"))

@app.route("/register")
def registerpage():
    return render_template("registerpage.html")

@app.route("/register", methods=["POST"])
def handleregister():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    confirm_password = request.form.get("confirm_password", None)
    if not username or not password or not confirm_password:
        flash("no username or password")
        redirect(url_for("registerpage"))
    if confirm_password != password:
        flash("the passwords do not match! please try again")
        return redirect(url_for("registerpage"))
    hash_value = generate_password_hash(password)
    sql_queries.add_users(username, hash_value)
    return redirect(url_for("loginpage"))

# homepage

@app.route("/home")
@authenticate
def home():
    posts = sql_queries.get_posts()
    user = sql_queries.right_profile(session["user_id"])
    return render_template("home.html", posts=posts, user=user, is_friend=is_friend)

@app.route("/likes/<int:post>", methods=["POST"])
@authenticate
def like(post):
    sql_queries.add_likes(post, session["user_id"])
    return redirect(request.referrer) # Reload the page

@app.route("/delete/<int:post>", methods=["POST"])
@authenticate
def delete_post(post):
    user_id = session.get("user_id")
    sql_queries.delete_post(post, user_id)
    return redirect(url_for("home"))

@app.route("/friends/<int:id>", methods=["POST"])
@authenticate
def friends(id):
    user_id = session["user_id"]
    sql_queries.add_friend(user_id, id)
    return redirect(url_for("home"))

# new post

@app.route("/new_post")
@authenticate
def new_post():
    return render_template("send_new_post.html")

@app.route("/send", methods=["POST"])
@authenticate
def add_posts():
    content = request.form.get("content", None)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    sql_queries.add_post(content, session["user_id"])
    return redirect(url_for("home"))

# profile

@app.route("/profile/<int:id>")
@authenticate
def profile(id):
    if not is_friend(id):
        flash("Not friends with the user :((")
        return redirect(url_for("home"))
    user = sql_queries.right_profile(id)
    bio = sql_queries.get_bio(id)
    posts = sql_queries.get_liked_posts(id)
    return render_template("profile.html", user=user, bio=bio, liked_posts=posts, is_friend=is_friend)

@app.route("/new_bio")
@authenticate
def new_bio():
    return render_template("add_bio.html")

@app.route("/add_bio", methods=["POST"])
@authenticate
def add_bio():
    bio = request.form.get("bio", None)
    sql_queries.add_bio(session["user_id"], bio)
    user_id = session["user_id"]
    return redirect(url_for("profile", id=user_id))

def is_friend(id):
    return session["user_id"] == id or sql_queries.profile_permission(session["user_id"], id)
