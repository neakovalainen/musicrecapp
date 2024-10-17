from sqlalchemy.sql import text
from db import db

def get_username(username):
    sql = text("""
        SELECT id, password
        FROM Users
        WHERE username = :username
    """)
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user

def add_users(username, hash_value):
    sql = text("""
        INSERT INTO Users (username, password)
        VALUES (:username, :password)
    """)
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

def get_likes():
    sql = text("""
        SELECT Posts.id, Posts.user_id as user_id, Posts.content, Posts.creation_time, Users.username, COUNT(Likes.id) as likes
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
    return posts

def add_post(content, user_id):
    sql = text("""
        INSERT INTO posts (content, user_id) 
        VALUES (:content, :user_id)
        RETURNING TRUE
    """)
    result = db.session.execute(sql, {"content":content, "user_id":user_id})
    success = result.fetchone() or False
    if success:
        db.session.commit()

def add_likes(post, user_id):
    sql = text("""
        INSERT INTO Likes (post_id, liker_id)
        VALUES (:post_id, :user_id)
        ON CONFLICT DO NOTHING
        RETURNING TRUE
    """)
    db.session.execute(sql, {"post_id":post, "user_id":user_id})
    db.session.commit()

def delete_post(post, user_id):
    sql = text("""
        DELETE FROM Posts
        WHERE id = :post_id
        AND user_id = :user_id
    """)
    db.session.execute(sql, {"post_id":post, "user_id":user_id})
    db.session.commit()

def profile_permission(user_id, friend_id):
    sql = text("""
        SELECT 1
        FROM Friends
        WHERE user_id = :user_id AND friend_id = :friend_id
    """)
    result = db.session.execute(sql, {"user_id":user_id, "friend_id":friend_id})
    return result.fetchone() is not None

def right_profile(user_id):
    sql = text("""
        SELECT id, username
        FROM Users
        WHERE id = :user_id
    """)
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def add_friend(user_id, friend_id):
    sql = text("""
        INSERT INTO Friends (user_id, friend_id)
        VALUES (:user_id, :friend_id)
        RETURNING TRUE
    """)
    db.session.execute(sql, {"user_id":user_id, "friend_id":friend_id})
    db.session.commit()

def add_bio(user_id, bio):
    sql = text("""
        INSERT INTO Bios (user_id, bio)
        VALUES (:user_id, :bio)
        ON CONFLICT (user_id) DO UPDATE
        SET bio = EXCLUDED.bio
    """)
    db.session.execute(sql, {"user_id":user_id, "bio":bio})
    db.session.commit()

def get_bio(user_id):
    sql = text("""
        SELECT bio
        FROM Bios
        WHERE user_id = :user_id
    """)
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()
