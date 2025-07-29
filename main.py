import subprocess
import os
import argparse
import shutil


# Set environment variable

# this enables debug logging for Ollama (disable this(set to 0) if you dont want your gpu/cpu logs)
os.environ["OLLAMA_DEBUG"] = "1"


def run_benchmark(model):

    # Define the command to run Ollama
    cmd = ["ollama", "serve"]
    cmd2 = ["python", "benchmark.py", "--model", f"{model}"]
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
            if process2.returncode != 0:
                print(
                    "Error running benchmark script check the model name---(llama3.1:8b,gemma2:2b,qwen2.5:7b)")
                exit(1)
            try:
                if os.environ["OLLAMA_DEBUG"] == "1" and process2.returncode == 0:
                    subprocess.run(cmd3)
            except Exception as e:
                print(f"Error running log_extractor.py: {e}")
                exit(1)
        except Exception as e:
            print(f"Error running benchmark script: {e}")
            exit(1)


def main():
    # stopping the ollama server if any started from the app or cli
    exsisting = subprocess.run(
        ["tasklist", "|", "findstr", "ollama"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if exsisting.stdout:
        subprocess.run(["powershell", "-Command",
                        "Stop-Process -Name 'ollama' -Force"])
    shutil.rmtree("ollama_debug.log", ignore_errors=True)

    parser = argparse.ArgumentParser(description="Run benchmark with model")
    parser.add_argument("--model", required=True,
                        help="Model name to benchmark (llama3.1, gemma2, qwen2.5)")

    args = parser.parse_args()

    run_benchmark(args.model)
    subprocess.run(["powershell", "-Command",
                    "Stop-Process -Name 'ollama' -Force"])


if __name__ == "__main__":
    main()
