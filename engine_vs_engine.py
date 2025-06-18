#!/usr/bin/env python3
"""
Play Stockfish-v-Stockfish and show each move on the console.
A complete PGN of the game is written to engine_vs_engine.pgn
"""

import chess, chess.engine, chess.pgn, time, shutil, pathlib, sys

# ---- EDIT ONLY THIS IF NEEDED ----
STOCKFISH_PATH = shutil.which("stockfish") or r"C:\Engines\stockfish.exe"
MOVE_TIME_S   = 0.1          # thinking time per move, in seconds
# ----------------------------------

def main():
    if not pathlib.Path(STOCKFISH_PATH).exists():
        sys.exit(f"Stockfish not found at {STOCKFISH_PATH!r}")

    print(f"Launching engines from {STOCKFISH_PATH}")
    white = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    black = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    board = chess.Board()
    game  = chess.pgn.Game()
    game.headers.update({
        "Event":      "Local SF 17.1 mirror match",
        "Site":       "localhost",
        "Date":       time.strftime("%Y.%m.%d"),
        "White":      "Stockfish 17.1",
        "Black":      "Stockfish 17.1",
        "TimeControl": f"{int(MOVE_TIME_S*1000)}+0",
    })
    node = game

    # Main loop ---------------------------------------------------------------
    while not board.is_game_over():
        engine = white if board.turn == chess.WHITE else black
        result = engine.play(board, chess.engine.Limit(time=MOVE_TIME_S))
        board.push(result.move)
        node = node.add_variation(result.move)

        # Pretty print the board after every move
        print(board, "\n", board.san(result.move), "\n" + "-"*60)
        time.sleep(0.15)  # slow it down so you can watch

    # Summary + cleanup -------------------------------------------------------
    outcome = board.result(claim_draw=True)
    print("Game over – result:", outcome)
    white.quit(); black.quit()

    with open("engine_vs_engine.pgn", "w", encoding="utf-8") as f:
        print(game, file=f)
    print("PGN saved to engine_vs_engine.pgn")

if __name__ == "__main__":
    main()
