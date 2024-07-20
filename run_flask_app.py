import subprocess
import time
import sys

# Use the Python executable from the currently activated environment
python_executable = sys.executable

while True:
    print("Starting Flask app...")
    process = subprocess.Popen([python_executable, r"E:\AI Ascending Software\AS AI Projects\AI facial analysis\AI-facial-analysis copy\app.py"])
    
    try:
        process.wait()
    except KeyboardInterrupt:
        print("Stopping Flask app...")
        process.terminate()
        process.wait()
    
    print("Flask app stopped. Restarting in immediately...")
    # time.sleep(1)
