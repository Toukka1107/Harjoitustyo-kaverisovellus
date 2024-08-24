from db import db
from sqlalchemy import text

def send_request(user_id, friend_id):
    sql = text("""
        INSERT INTO friend_requests (sender_id, receiver_id)
        VALUES (:sender_id, :receiver_id)
        """)
    try:
        db.session.execute(sql, {"sender_id": user_id, "receiver_id": friend_id})
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def delete_friend_request(sender_id: int, receiver_id: int):
    sql = text("""
        DELETE FROM friend_requests
        WHERE sender_id = :sender_id AND receiver_id = :receiver_id
        """)
    db.session.execute(sql, {"sender_id": sender_id, "receiver_id": receiver_id})
    db.session.commit()

def get_friend_request(sender_id: int, receiver_id: int):
    sql = text("""
        SELECT fr.id FROM friend_requests fr
        WHERE sender_id = :sender_id AND receiver_id = :receiver_id
        """)
    return db.session.execute(sql, {"sender_id": sender_id, "receiver_id": receiver_id}).fetchone()

def get_all_friend_requests(receiver_id: int):
    sql = text("""
        SELECT u.username
        FROM friend_requests fr
        JOIN users u ON u.id = fr.sender_id
        WHERE fr.receiver_id = :receiver_id
        """)
    return db.session.execute(sql, {"receiver_id": receiver_id}).fetchall()

def add_friends(user_id: int, friend_id: int):
    sql = text("""
        INSERT INTO friends (user_id, friend_id)
        VALUES (:user_id, :friend_id)
        """)
    
    db.session.execute(sql, {"user_id": user_id, "friend_id": friend_id})
    db.session.execute(sql, {"user_id": friend_id, "friend_id": user_id})

    sql = text("""
        DELETE FROM friend_requests
        WHERE sender_id = :sender_id AND receiver_id = :receiver_id
        """)
    db.session.execute(sql, {"sender_id": friend_id, "receiver_id": user_id})

    db.session.commit()

def delete_friend(user_id: int, friend_id: int):
    sql = text("""
               DELETE FROM friends
               WHERE user_id = :user_id AND friend_id = :friend_id
               """)
    
    try:
        db.session.execute(sql, {"user_id": user_id, "friend_id": friend_id})
        db.session.execute(sql, {"user_id": friend_id, "friend_id": user_id})
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def get_all_friends(user_id: int):
    sql = text("""
        SELECT DISTINCT u.username
        FROM friends f
        JOIN users u ON (f.user_id = u.id OR f.friend_id = u.id)
        WHERE (f.user_id = :user_id OR f.friend_id = :user_id)
        AND u.id != :user_id
        """)
    return db.session.execute(sql, {"user_id": user_id}).fetchall()

def check_friend_request(user_id: int, friend_id: int):
    sql = text("""
        SELECT id
        FROM friend_requests
        WHERE sender_id = :user_id AND receiver_id = :friend_id
        """)
    result = db.session.execute(sql, {"user_id": user_id, "friend_id": friend_id}).fetchone()
    if result:
        return True
    else:
        return None

def check_friendship(user_id: int, friend_id: int):
    sql = text("""
        SELECT 1
        FROM friends
        WHERE user_id = :user_id AND friend_id = :friend_id
               OR user_id = :friend_id AND friend_id = :user_id
        """)

    result = db.session.execute(sql, {"user_id": user_id, "friend_id": friend_id}).fetchone()
    if result:
        return True
    else:
        return None
