#!/usr/bin/env python
"""
Local web viewer – Stockfish-vs-Stockfish (Windows / Python 3.12)

How to run
----------
# (inside the repo root)
python -m venv venv
venv\Scripts\activate
pip install flask==3.0.2 flask-socketio==5.3.6 eventlet==0.36.1 python-chess==1.999
python app.py

Then open http://localhost:5000 in your browser.
"""

import pathlib, time, threading
import chess, chess.engine
from flask import Flask, render_template
from flask_socketio import SocketIO

# ── SETTINGS ──────────────────────────────────────────────────────────────
ENGINE_PATH   = pathlib.Path("engines/stockfish.exe")   # path to engine exe
MOVE_TIME_SEC = 0.3                                     # thinking time / move
# ──────────────────────────────────────────────────────────────────────────

if not ENGINE_PATH.exists():
    raise SystemExit(
        f"⚠ Stockfish not found at {ENGINE_PATH}\n"
        "Download Stockfish 17.1 (Windows AVX2 build) from "
        "https://stockfishchess.org/download/ and place stockfish.exe there."
    )

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app)        # eventlet is okay on Python 3.12

@app.route("/")
def index():
    return render_template("index.html")

def play_match():
    """Run one Stockfish-versus-Stockfish game and stream FENs to the client."""
    board = chess.Board()
    white = chess.engine.SimpleEngine.popen_uci(str(ENGINE_PATH))
    black = chess.engine.SimpleEngine.popen_uci(str(ENGINE_PATH))

    while not board.is_game_over():
        engine = white if board.turn == chess.WHITE else black
        move   = engine.play(board, chess.engine.Limit(time=MOVE_TIME_SEC)).move
        board.push(move)
        socketio.emit("move", {"fen": board.fen()})   # broadcast to browser
        time.sleep(0.1)                              # smooth animation

    socketio.emit("game_over", {"result": board.result()})
    white.quit(); black.quit()

if __name__ == "__main__":
    threading.Thread(target=play_match, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000)
