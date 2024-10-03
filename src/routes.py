from app import app
import sql_queries
from flask import redirect, render_template, request, session, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash

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
    sql_queries.add_users(username, hash_value)
    return redirect("/")

@app.route("/home")
def home():
    # add link/ button to the search thing
    posts = sql_queries.get_likes()
    print(posts)
    return render_template("home.html", posts=posts)

@app.route("/likes/<int:post>", methods=["POST"])
def like(post):
    sql_queries.add_likes(post, session["user_id"])
    return redirect(url_for("home"))

@app.route("/new_post")
def new_post():
    return render_template("send_new_post.html")

@app.route("/send", methods=["POST"])
def add_posts():
    content = request.form["content"]
    sql_queries.add_post(content, session["user_id"])
    return redirect(url_for("home"))

@app.route("/profile")
def profile():
    # does the user have a premission to view the profile?
    return render_template("profile.html")

@app.route("/search") # no need to add get? -> might just add anyway
def search():
    pass
# add searchbar, can search by user or by word in post/song or smth
