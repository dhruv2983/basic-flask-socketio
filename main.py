from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app)

CORS(app, resources={r"/": {"origins": "*"}})


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("message")
def handle_message(data):
    try:
        emit("message", data + 5)
    except Exception as e:
        print(f"Error handling message: {e}")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
