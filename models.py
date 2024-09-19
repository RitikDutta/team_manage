#connection establishement
from flask_login import UserMixin
from config import DB_CONFIG
import mysql.connector

class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

def load_user(user_id):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        return User(user_id=user['user_id'], username=user['username'], role=user['role'])
    return None
