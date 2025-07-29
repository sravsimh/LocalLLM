import subprocess
import os

# Set environment variable

# this enables debug logging for Ollama (disable this(set to 0) if you dont want your gpu/cpu logs)
os.environ["OLLAMA_DEBUG"] = "1"

# Define the command to run Ollama
cmd = ["ollama", "serve"]
cmd2 = ["python", "benchmark.py"]
cmd3 = ["python", "log_extractor.py"]

with open("ollama_debug.log", "w", encoding="utf-8") as log_file:
    # Start Ollama server
    try:
        process = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            env=os.environ
        )
    except Exception as e:
        print(f"Error starting Ollama server: {e}")
        exit(1)

    # Running benchmark.py script
    try:
        process2 = subprocess.run(cmd2)

    except Exception as e:
        print(f"Error running benchmark script: {e}")
        exit(1)

    # stopping the ollama server
    subprocess.run(["powershell", "-Command",
                   "Stop-Process -Name 'ollama' -Force"])
    if os.environ["OLLAMA_DEBUG"] == "1":
        subprocess.run(cmd3)

print("data is in json file and logs are in ollama_debug.log")
