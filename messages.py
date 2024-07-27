from db import db
from datetime import datetime, timezone
from sqlalchemy import text

def message(user_id, subject, content):
    current_time = datetime.now(timezone.utc)
    sql = text("INSERT INTO messages (user_id, subject, message, time) VALUES (:user_id, :subject, :message, :time)")
    db.session.execute(sql, {"user_id": user_id, "subject": subject, "message": content, "time": current_time})
    db.session.commit()
    return True

    
def all_messages():
    sql = text("""SELECT messages.id, messages.subject, messages.message, messages.time, users.username 
                    FROM messages 
                    JOIN users ON messages.user_id = users.id 
                    ORDER BY messages.time DESC""")
    return db.session.execute(sql).fetchall()

def generate_message_id():
    result = db.session.execute(text("SELECT MAX(id) FROM messages"))
    max_id = result.scalar() or 0
    return max_id + 1
