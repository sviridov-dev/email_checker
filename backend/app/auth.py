from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql
from passlib.hash import bcrypt
import jwt, os
from functools import wraps

auth = Blueprint('auth', __name__)

def token_compare(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            # let assume that only one user is on the user table
            cur = mysql.connection.cursor()
            cur.execute("SELECT session_token FROM users LIMIT 1")
            user = cur.fetchone()
            cur.close()
            if not user:
                return jsonify({'error': 'No user found'}), 401
            elif user[0] != '':
                return jsonify({'error': 'Session expired (another login detected)'}), 403
            else:
                # If token is empty, we assume the user is not logged in
                return f(*args, **kwargs)
        else:
            try:
                data = jwt.decode(token,  os.getenv("SECRET_KEY"), algorithms=["HS256"])
                user_id = data['user_id']
            except:
                return jsonify({'error': 'Invalid token'}), 401

            cur = mysql.connection.cursor()
            cur.execute("SELECT session_token FROM users WHERE id=%s", (user_id,))
            user = cur.fetchone()
            cur.close()

            if not user or user[0] != token:
                return jsonify({'error': 'Session expired (another login detected)'}), 403

            return f(*args, **kwargs)
    return decorated

@auth.route('/api/create', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    hashed_password = generate_password_hash(password)
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "ok"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth.route('/api/login', methods=['POST'])
@token_compare
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username=%s", (username,))
    user = cur.fetchone()

    if not user:
        return jsonify({"error": "Unregister"}), 401  # 401 Unauthorized is more appropriate

    user_id, password_hash = user

    if not check_password_hash(password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({"user_id": user_id}, os.getenv("SECRET_KEY"), algorithm="HS256")

    cur.execute("UPDATE users SET session_token=%s WHERE id=%s", (token, user_id))
    mysql.connection.commit()

    return jsonify({"token": token})


