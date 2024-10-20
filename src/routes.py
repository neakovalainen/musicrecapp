from flask import redirect, render_template, request, session, url_for, flash, abort
from werkzeug.security import check_password_hash, generate_password_hash
import sql_queries
import secrets
from app import app

@app.route("/", methods=["GET"])
def loginpage():
    return render_template("loginpage.html", title="login")

@app.route("/", methods=["POST"])
def handlelogin():
    username = request.form["username"]
    password = request.form["password"]
    user = sql_queries.get_username(username)
    if not user:
        flash("incorrect username or password")
        return redirect("/")
    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["user_id"] = user.id
        session["csrf_token"] = secrets.token_hex(16)
        print(f"User: {username} logging in with password: {password}")
        return redirect(url_for("home"))

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
    sql_queries.add_users(username, hash_value)
    return redirect("/")

@app.route("/home")
def home():
    # add link/ button to the search thing
    posts = sql_queries.get_posts()
    print([post.user_id for post in posts])
    user = sql_queries.right_profile(session["user_id"])
    print(posts)
    return render_template("home.html", posts=posts, user=user, is_friend=is_friend)

@app.route("/likes/<int:post>", methods=["POST"])
def like(post):
    sql_queries.add_likes(post, session["user_id"])
    # Reload the page
    return redirect(request.referrer)
    # return redirect(url_for("home"))

@app.route("/new_post")
def new_post():
    return render_template("send_new_post.html")

@app.route("/send", methods=["POST"])
def add_posts():
    content = request.form["content"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    else:
        print("workkk")
    sql_queries.add_post(content, session["user_id"])
    return redirect(url_for("home"))

@app.route("/delete/<int:post>", methods=["POST"])
def delete_post(post):
    user_id = session.get("user_id")
    sql_queries.delete_post(post, user_id)

    return redirect(url_for("home"))

@app.route("/profile/<int:id>")
def profile(id):
    if not is_friend(id):
        flash("Not friends with the user :((")
        return redirect(url_for("home"))
    user = sql_queries.right_profile(id)
    bio = sql_queries.get_bio(id)
    posts = sql_queries.get_liked_posts(id)
    return render_template("profile.html", user=user, bio=bio, liked_posts=posts, is_friend=is_friend)

def is_friend(id):
    print(id)
    return session["user_id"] == id or sql_queries.profile_permission(session["user_id"], id)

@app.route("/new_bio")
def new_bio():
    return render_template("add_bio.html")

@app.route("/add_bio", methods=["POST"])
def add_bio():
    bio = request.form["bio"]
    sql_queries.add_bio(session["user_id"], bio)
    user_id = session["user_id"]
    return redirect(url_for("profile", id=user_id))


@app.route("/friends/<int:id>", methods=["POST"])
def friends(id):
    user_id = session["user_id"]
    sql_queries.add_friend(user_id, id)
    return redirect(url_for("home"))

@app.route("/search") # no need to add get? -> might just add anyway
def search():
    pass
# add searchbar, can search by user or by word in post or smth
