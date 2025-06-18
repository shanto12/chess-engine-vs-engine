#!/usr/bin/env python
r"""
Local web viewer – Stockfish‑vs‑Stockfish (Windows / Python 3.12)

Quick start
-----------
# At a PowerShell prompt in the repo root
python -m venv venv
venv\Scripts\activate
pip install flask==3.0.2 flask-socketio==5.3.6 eventlet==0.36.1 python-chess==1.999
python app.py          # ◀ starts http://localhost:5000
"""

import pathlib, time, threading
import chess, chess.engine
from flask import Flask, render_template
from flask_socketio import SocketIO

# ── SETTINGS ──────────────────────────────────────────────────────────────
ENGINE_PATH   = pathlib.Path("engines/stockfish.exe")   # where you put SF 17.1
MOVE_TIME_SEC = 0.3                                     # think time per move
# ──────────────────────────────────────────────────────────────────────────

if not ENGINE_PATH.exists():
    raise SystemExit(
        f"⚠ Stockfish not found at {ENGINE_PATH}\n"
        "Download the Windows AVX2 build from https://stockfishchess.org/download/ "
        "and rename the exe to stockfish.exe inside the engines/ folder."
    )

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app)        # eventlet driver works fine on Python ≤ 3.12

@app.route("/")
def index():
    return render_template("index.html")

def play_match():
    """Run one Stockfish‑vs‑Stockfish game and stream FENs to the browser."""
    board = chess.Board()
    white = chess.engine.SimpleEngine.popen_uci(str(ENGINE_PATH))
    black = chess.engine.SimpleEngine.popen_uci(str(ENGINE_PATH))

    while not board.is_game_over():
        engine = white if board.turn == chess.WHITE else black
        move   = engine.play(board, chess.engine.Limit(time=MOVE_TIME_SEC)).move
        board.push(move)
        socketio.emit("move", {"fen": board.fen()})
        time.sleep(0.1)                   # smooth animation

    socketio.emit("game_over", {"result": board.result()})
    white.quit(); black.quit()

if __name__ == "__main__":
    threading.Thread(target=play_match, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000)
