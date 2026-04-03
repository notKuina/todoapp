# run.py
import os
import webbrowser
from threading import Timer
from app import app

def open_browser():
    """Open the app in the default web browser (desktop mode)."""
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    # Check if running locally
    if os.environ.get("FLASK_ENV") != "production":
        # Open browser only for local desktop usage
        Timer(1, open_browser).start()
        app.run(debug=True, host="127.0.0.1", port=5000)
    else:
        # For online hosting (hosted servers provide their own host/port)
        # Do NOT open browser automatically
        app.run()