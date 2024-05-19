from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS
from flask_session import Session
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'redis'  # Use 'redis' or 'memcached' for production
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session lifetime in seconds

Session(app)
socketio = SocketIO(app, manage_session=False)  # Let Flask-Session handle sessions
CORS(app, resources={r"/": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    session_id = request.sid
    if 'user' not in session:
        logger.info(f"Invalid session {session_id}, disconnecting")
        disconnect()
    else:
        logger.info(f"Valid session {session_id}")

@socketio.on("disconnect")
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on("message")
def handle_message(data):
    try:
        if 'user' not in session:
            logger.info(f"Invalid session {request.sid}, disconnecting")
            disconnect()
        else:
            logger.info(f"Message from {request.sid}: {data}")
            emit("message", data + 5)
    except Exception as e:
        logger.error(f"Error handling message: {e}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
