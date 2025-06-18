#!/usr/bin/env python
"""
Local web viewer: Stockfish-vs-Stockfish (Windows edition)
Run:  python app.py
Then browse to http://localhost:5000
"""
import pathlib, time, threading, chess, chess.engine
from flask import Flask, render_template
from flask_socketio import SocketIO

# ── SETTINGS ────────────────────────────────────────────────
ENGINE_PATH   = pathlib.Path("engines/stockfish.exe")   # relative to repo root
MOVE_TIME_SEC = 0.3                                     # thinking time per move
# ────────────────────────────────────────────────────────────

if not ENGINE_PATH.exists():
    raise SystemExit(f"⚠ Stockfish not found at {ENGINE_PATH}. "
                     "Download 17.1 - Windows AVX2 build and place stockfish.exe there.")

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app)  # enables websockets

@app.route("/")
def index():
    return render_template("index.html")

def play_match():
    board = chess.Board()
    white = chess.engine.SimpleEngine.popen_uci(str(ENGINE_PATH))
    black = chess.engine.SimpleEngine.popen_uci(str(ENGINE_PATH))

    while not board.is_game_over():
        engine = white if board.turn == chess.WHITE else black
        move   = engine.play(board, chess.engine.Limit(time=MOVE_TIME_SEC)).move
        board.push(move)
        socketio.emit("move", {"fen": board.fen()})
        time.sleep(0.1)                     # smooth updates

    socketio.emit("game_over", {"result": board.result()})
    white.quit(); black.quit()

if __name__ == "__main__":
    threading.Thread(target=play_match, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000)
