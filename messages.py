from db import db
from datetime import datetime, timezone
from sqlalchemy import text

def add_message(user_id, subject, content):
    current_time = datetime.now(timezone.utc)
    sql = text("INSERT INTO messages (user_id, subject, message, time) VALUES (:user_id, :subject, :message, :time)")
    db.session.execute(sql, {"user_id": user_id, "subject": subject, "message": content, "time": current_time})
    db.session.commit()

def all_messages():
    sql = text("""SELECT m.id, m.user_id, m.subject, m.message, m.time, u.username, p.avatar
                    FROM messages m
                    JOIN users u ON m.user_id = u.id
                    JOIN profiles p ON m.user_id = p.user_id
                    ORDER BY m.time DESC""")
    original_messages = db.session.execute(sql).fetchall()

    conversations = []

    for message in original_messages:
        comments = all_comments(message.id)
        message_time = message.time.strftime("%H:%M %d/%m/%y")
        conversations.append({"id": message.id, "user_id": message.user_id, "subject": message.subject, "message": message.message, "time": message_time, "username": message.username, "comments": comments, "avatar": message.avatar})

    return conversations

def add_comment(user_id, message_id, content):
    current_time = datetime.now(timezone.utc)
    sql = text("INSERT INTO comments (user_id, message_id, comment, time) VALUES (:user_id, :message_id, :comment, :time)")
    db.session.execute(sql, {"user_id": user_id, "message_id": message_id, "comment": content, "time": current_time})
    db.session.commit()

def all_comments(message_id):
    sql = text("""SELECT c.comment, c.time, u.username 
                  FROM comments c 
                  JOIN users u ON c.user_id = u.id 
                  WHERE c.message_id = :message_id 
                  ORDER BY c.time ASC""")
    comments = db.session.execute(sql, {"message_id": message_id}).fetchall()

    formatted_comments = []
    for comment in comments:
        comment_time = comment.time.strftime("%H:%M %d/%m/%y")
        formatted_comments.append({
            "comment": comment.comment,
            "time": comment_time,
            "username": comment.username
        })

    return formatted_comments
