from flask import Flask, render_template, send_from_directory, session, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import random
import datetime
import os
from functools import wraps
import hashlib
import re
import html
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import sys
from io import StringIO

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['APPLICATION_ROOT'] = '/ciallosecurity'
app.config['SECRET_KEY'] = 'your-secret-key'  
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(hours=24)
)

socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   path='/ciallosecurity/socket.io')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

log_stream = StringIO()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(log_stream)
    ]
)
logger = logging.getLogger(__name__)

def init_db():
    db_path = os.path.join(BASE_DIR, 'chat.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  message TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_random_name():
    names_path = os.path.join(BASE_DIR, 'names.txt')
    with open(names_path, 'r', encoding='utf-8') as f:
        names = f.read().splitlines()
    return random.choice(names)

def handle_db_error(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
            return None
    return decorated_function

@handle_db_error
def get_chat_history():
    db_path = os.path.join(BASE_DIR, 'chat.db')
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('SELECT username, message, timestamp FROM messages ORDER BY timestamp')
        return c.fetchall()

@app.route('/ciallosecurity/')
def index():
    username = get_random_name()
    session['username'] = username
    chat_history = get_chat_history()
    return render_template('index.html', username=username, chat_history=chat_history)

def require_username(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return {'error': 'No username in session'}, 400
        return f(*args, **kwargs)
    return decorated_function

def sanitize_message(message):
    if not message:
        return ''
    return message[:500]

@socketio.on('send_message')
@require_username
def handle_message(data):
    username = session.get('username')
    message = sanitize_message(data.get('message', ''))
    
    if not message or len(message.strip()) == 0:
        return
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"用户 {username} 发送消息: {message}")  
    
    db_path = os.path.join(BASE_DIR, 'chat.db')
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)',
                    (username, message, timestamp))
            conn.commit()
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return
    
    emit('receive_message', {
        'username': username,
        'message': message,
        'timestamp': timestamp
    }, broadcast=True)

@app.route('/ciallosecurity/favicon.ico')
def favicon():
    return send_from_directory(BASE_DIR,
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/ciallosecurity/logs')
def get_logs():
    return jsonify({'logs': log_stream.getvalue()})

@socketio.on('connect')
def handle_connect():
    logger.info(f"用户 {session.get('username', 'Unknown')} 已连接")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"用户 {session.get('username', 'Unknown')} 已断开连接")

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True, host='0.0.0.0', port=43816)
