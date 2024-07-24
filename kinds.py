import subprocess
import time
import sys

# Use the Python executable from the currently activated environment
python_executable = sys.executable

def restart_app():
    process = subprocess.Popen([python_executable, r"E:\AI Ascending Software\AS AI Projects\AI facial analysis\AI-facial-analysis\app.py"])
    try:
        process.wait()
    except KeyboardInterrupt:
        print("Stopping Flask app...")
        process.terminate()
        process.wait()
    
    print("Flask app stopped. Restarting in immediately...")