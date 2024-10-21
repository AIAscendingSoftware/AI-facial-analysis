'rerun app after completing process and return the respones after completing process'
import subprocess
import time
import sys
import os

# Use the Python executable from the currently activated environment
python_executable = sys.executable
app_path = r"D:\AI Projects\AI Facial Analysis\AI-facial-analysis\app.py"

def run_app():
    print("Starting Flask app...")
    process = subprocess.Popen([python_executable, app_path])

    while True:
        try:
            time.sleep(1)
            if os.path.exists("restart.txt"):
                print("Restart file detected. Restarting Flask app...")
                os.remove("restart.txt")
                process.terminate()
                process.wait()
                run_app()
                break
        except KeyboardInterrupt:
            print("Stopping Flask app...")
            process.terminate()
            process.wait()
            sys.exit(0)  # Exit the script on keyboard interrupt

while True:
    run_app()
    time.sleep(1)  # Short delay before restarting


# 'rerun app after getting error ad return the respones after completing process'
# import subprocess
# import time
# import sys

# # Use the Python executable from the currently activated environment
# python_executable = sys.executable

    
# while True:
#     print("Starting Flask app...")
#     process = subprocess.Popen([python_executable, r"E:\AI Ascending Software\AS AI Projects\AI facial analysis\AI-facial-analysis\app.py"])
    
#     try:
#         process.wait()
#     except KeyboardInterrupt:
#         print("Stopping Flask app...")
#         process.terminate()
#         process.wait()
    
#     print("Flask app stopped. Restarting in immediately...")
#     # time.sleep(1)



# 'rerun app after completing process amd return the respones immediately'
# import subprocess
# import time
# import sys

# # Use the Python executable from the currently activated environment
# python_executable = sys.executable
# app_path = r"E:\AI Ascending Software\AS AI Projects\AI facial analysis\AI-facial-analysis\app.py"

# def run_app():
#     print("Starting Flask app...")
#     process = subprocess.Popen([python_executable, app_path])
    
#     try:
#         exit_code = process.wait()
#         print(f"Flask app exited with code {exit_code}. Restarting...")
#     except KeyboardInterrupt:
#         print("Stopping Flask app...")
#         process.terminate()
#         process.wait()
#         sys.exit(0)  # Exit the script on keyboard interrupt

# while True:
#     run_app()
#     time.sleep(1)  # Short delay before restarting



