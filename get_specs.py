from glob import glob
import subprocess
import shutil
import platform
import psutil
import GPUtil
import json
import os
import questionary
import signal

from sqlalchemy import Null

snake_process = None
models_selected = []
CONFIG_FILE = "ollama_setup_complete.json"

MODELS = {
    "gemma:2b": "Gemma 2B (No GPU)",
    "gemma:7b": "Gemma 7B (GPU)",
    "llama3.1:8b": "LLaMA 3.1 8B (GPU)",
    "qwen2.5:0.5b": "Qwen 2.5 0.5B (No GPU)",
    "qwen2.5:1.5b": "Qwen 2.5 1.5B (No GPU)",
    "qwen2.5:3b": "Qwen 2.5 3B (No GPU)",
    "qwen2.5:7b": "Qwen 2.5 7B (GPU)",

}


def is_ollama_installed():
    return shutil.which("ollama") is not None


def get_system_info():
    info = {
        "CPU": platform.processor(),
        "Cores": psutil.cpu_count(logical=False),
        "Logical Cores": psutil.cpu_count(logical=True),
        "Memory (GB)": round(psutil.virtual_memory().total / (1024**3), 2)
    }

    # Add disk space (assuming C:\ for Windows or / for others)
    partition = "C:\\" if os.name == "nt" else "/"
    disk = psutil.disk_usage(partition)
    info["Disk Total (GB)"] = round(disk.total / (1024**3), 2)
    info["Disk Free (GB)"] = round(disk.free / (1024**3), 2)

    # GPU info
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        info.update({
            "GPU": gpu.name,
            "GPU Memory (Total GB)": round(gpu.memoryTotal / 1024, 2),
            "GPU Memory (Free GB)": round(gpu.memoryFree / 1024, 2)
        })
    else:
        info["GPU"] = None

    return info


def print_system_info():
    print("\n System Information:")
    sys_info = get_system_info()
    for k, v in sys_info.items():
        print(f"{k}: {v}")
    print()


def select_models():
    choices = [{"name": name, "value": model}
               for model, name in MODELS.items()]
    selected = questionary.checkbox(
        "Select model(s) based on your system specifications to pull:",
        choices=choices
    ).ask()

    return selected or []


def run_snake_game():
    global snake_process
    try:
        subprocess.run(["pip", "install", "ruben-snake-cmd"], check=True)

        system = platform.system()
        is_wsl = "microsoft" in platform.uname().release.lower()

        if system == "Windows" or is_wsl:
            snake_process = subprocess.Popen([
                "cmd.exe", "/c", "start", "cmd", "/k", "ruben-snake-cmd"
            ])
            print("Snake game launched in new terminal (Windows/WSL)")
        elif system == "Linux":
            terminal = shutil.which(
                "gnome-terminal") or shutil.which("x-terminal-emulator") or shutil.which("konsole")
            if terminal:
                snake_process = subprocess.Popen(
                    [terminal, "--", "bash", "-c", "ruben-snake-cmd; exec bash"])
                print("Snake game launched in new terminal (Linux)")
            else:
                print("No supported terminal emulator found.")
        elif system == "Darwin":
            apple_script = '''
            tell application "Terminal"
                do script "ruben-snake-cmd"
                activate
            end tell
            '''
            snake_process = subprocess.Popen(["osascript", "-e", apple_script])
            print("Snake game launched in new terminal (macOS)")
        else:
            print("Unsupported platform.")
    except Exception as e:
        print(f"Could not launch Snake game: {e}")


def stop_snake_game():
    global snake_process
    try:
        # Kill by process name instead of relying on terminal pid
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'ruben-snake-cmd' in ' '.join(proc.info.get('cmdline') or []):
                proc.kill()
                print(f"Terminated Snake game process: PID {proc.pid}")
    except Exception as e:
        print(f"Error stopping Snake game: {e}")


def pull_models(models):
    play_game = questionary.confirm(
        "Do you want to play Snake while models are downloading?").ask()

    try:
        if play_game:
            run_snake_game()
        for model in models:
            print(f"\nPulling model: {model} ...")
            subprocess.run(["ollama", "pull", model])
    finally:
        if play_game:
            print("\nStopping Snake game...")
            stop_snake_game()


def save_setup_complete():
    info = get_system_info()
    info["models"] = models_selected
    with open(CONFIG_FILE, "w") as f:
        json.dump({"setup_complete": True, "info": info}, f)


def setup_already_done():
    return os.path.isfile(CONFIG_FILE)


def main():
    global models_selected
    if setup_already_done():
        print(" Ollama setup already completed. Skipping setup.")
        return

    if not is_ollama_installed():
        print(" Ollama is not installed. Please install it from https://ollama.com/")
        return

    print_system_info()

    selected_models = select_models()
    models_selected = selected_models
    if not selected_models:
        print(" No models selected. Exiting.")
        return

    pull_models(selected_models)
    save_setup_complete()
    print("\n Ollama setup complete. You can now use the selected models.")


if __name__ == "__main__":
    main()
