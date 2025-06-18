# Stockfish-vs-Stockfish Web Viewer (Windows)

Small Flask app that lets you watch two copies of Stockfish 17.1 play each
other in real time via a browser.

## Prerequisites
* **Python 3.9 +** (`py --version`)
* **Stockfish 17.1** Windows AVX2 build – download from
  <https://stockfishchess.org/download/> and place `stockfish.exe` in
  `engines/`.

## Quick start
```powershell
# create & activate virtual-env (optional but recommended)
py -m venv venv
venv\Scripts\activate

# install Python deps
pip install -r requirements.txt

# run the app
python app.py
