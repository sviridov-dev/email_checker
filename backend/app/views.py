# app/views.py
from flask import Flask, Blueprint, request, jsonify, send_from_directory
from app.imap_checker import check_email_status
from app import mysql
import os, jwt

from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

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



main = Blueprint('main', __name__)




@main.route('/api/emails', methods=['GET'])
@token_required
def get_emails():

    cur = mysql.connection.cursor()
    cur.execute("SELECT id,email FROM check_email_address ORDER BY id ASC LIMIT 10")
    address_info = cur.fetchall()
    result = []
    for acc in address_info:
        result.append({"id": acc[0], "email": acc[1]})
        
    return jsonify({"status": "OK", "results": result})



@main.route('/api/check', methods=['POST'])
@token_required
def check_email():


    data = request.json
    from_name_or_email = data.get("search")
    account_email = data.get("email")

    cur = mysql.connection.cursor()
    cur.execute("SELECT password FROM check_email_address WHERE email = %s", (account_email,))
    account_email_info = cur.fetchone()
    cur.close()

    results = []
    inbox_num = 0
    spam_num = 0
    nofind_num = 0
    # for acc in address_info:
    # Check email status for each account
    status_list = check_email_status(account_email, account_email_info[0], from_name_or_email)
    # inbox_num += status_list["inbox"]
    # spam_num += status_list["spam"]
    # nofind_num += status_list["not_found"]

    # cur.close()
    # all_box = inbox_num + spam_num + nofind_num
    # p_inbox = round((inbox_num/(all_box)) * 100, 2) if all_box > 0 else 0
    # p_spam = round((spam_num/(all_box)) * 100, 2) if all_box > 0 else 0
    return jsonify({"status": "OK", "results": status_list})

@main.route("/api/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Missing token"}), 401

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET session_token = NULL WHERE session_token = %s", (token,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "OK", "message": "Logout success"}), 200

# Protected Route Example
@main.route("/api/profile", methods=["GET"])
@token_required
def profile(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"id": user["id"], "username": user["username"]})