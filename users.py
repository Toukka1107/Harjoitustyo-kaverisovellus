from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    
    if result is None:
        return False
    
    user_id, stored_password = result
    
    if check_password_hash(stored_password, password):
        session["user_id"] = user_id
        return True
    else:
        return False

def logout():
    session.pop("user_id", None)

def signup(username, password, age, hobbies, about_me):
    hash = generate_password_hash(password)
    user_id = generate_user_id()
    
    sql_users = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql_users, {"username": username, "password": hash})
    
    sql_profile = text("INSERT INTO profiles (user_id, age, hobbies, about_me) VALUES (:user_id, :age, :hobbies, :about_me)")
    db.session.execute(sql_profile, {"user_id": user_id, "age": age, "hobbies": hobbies, "about_me": about_me})
    
    db.session.commit()
    return login(username, password)

def edit_profile(user_id, age, hobbies, about_me):
    try:
        sql = text("UPDATE profiles SET age = :age, hobbies = :hobbies, about_me = :about_me WHERE user_id = :user_id")
        db.session.execute(sql, {"age": age, "hobbies": hobbies, "about_me": about_me, "user_id": user_id})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False 

def generate_user_id():
    result = db.session.execute(text("SELECT MAX(id) FROM users")).fetchone()
    max_id = result[0] if result and result[0] is not None else 0
    return max_id + 1

def get_user_id():
    return session.get("user_id", 0)

def get_username(user_id):
    sql = text("SELECT username FROM users WHERE id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    return result[0] if result else None

def get_profile_by_user_id(user_id):
    sql = text("""
        SELECT age, hobbies, about_me
        FROM profiles
        WHERE user_id = :user_id
        """)
    return db.session.execute(sql, {"user_id": user_id}).fetchone()

def get_user_by_username(username):
    sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    return result[0] if result else None

def check_username(username):
    sql = text("SELECT username FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username}).fetchone()

    return True if result else False
    
