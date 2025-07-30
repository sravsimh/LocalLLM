import subprocess
import os
import questionary
import psutil
import json
import argparse

CONFIG_FILE = "ollama_setup_complete.json"

# Enable debug logging for Ollama (disable this by setting to "0")
os.environ["OLLAMA_DEBUG"] = "1"
sys_info = {}

OLLAMA_LOG = "ollama_debug.log"


def run_benchmark(model):
    cmd_benchmark = ["python", "benchmark.py", "--model", f"{model}"]

    with open(OLLAMA_LOG, "w", encoding="utf-8") as log_file:
        try:
            process2 = subprocess.run(cmd_benchmark)

            if process2.returncode != 0:
                print(
                    "Error running benchmark script. Check the model name (llama3.1:8b, gemma2:2b, qwen2.5:7b)")

                exit(1)
            else:
                print(f"Benchmark completed for model: {model}")

        except Exception as e:
            print(f"Error running benchmark script: {e}")

            exit(1)


def setup_already_done():
    return os.path.isfile(CONFIG_FILE)


def clean_log():
    if os.path.isfile(OLLAMA_LOG):
        os.remove(OLLAMA_LOG)


def main():
    global sys_info

    files_to_delete = [
        "stats.json",
        "benchmark_results.csv",
        "Avg_benchmark_results.csv"
    ]

    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
                exit(1)

    clean_log()

    parser = argparse.ArgumentParser(description="Run benchmark with model")
    parser.add_argument("--model", required=False,
                        help="Model name to benchmark (llama3.1:8b, gemma2:2b, qwen2.5:7b)")
    args = parser.parse_args()

    if (args.model):
        if os.path.exists("stats.json"):
            if (args.model in sys_info['info']['models']):
                run_benchmark(args.model)
            else:
                print(
                    f"download model to run benchmarks: ollama pull {args.model}")
                exit(1)
        else:
            print(
                f"download model to run benchmarks: ollama pull {args.model}")
            exit(1)
    else:
        if os.path.exists("stats.json"):
            with open("stats.json", "r") as f:
                sys_info = json.load(f)
        else:
            subprocess.run(["python", "get_specs.py"])
            with open("stats.json", "r") as f:
                sys_info = json.load(f)
        if len(sys_info['info']['models']) > 0:
            for model in sys_info["info"]["models"]:
                print(f"Running benchmark for model: {model}")
                run_benchmark(model)
        else:
            print("No models found in stats.json. Please run get_specs.py first.")
            os.remove("stats.json")
            exit(1)

    print("please check the CSV and Detailed_benchmark.json file for benchmarks")

    re_run = questionary.confirm(
        "do you want to re-run or test other models").ask()

    if re_run:
        os.remove("stats.json")
        os.remove("Detailed_benchmark.json")
        os.remove("benchmark_results.csv")
        os.remove("Avg_benchmark_results.csv")
        main()


if __name__ == "__main__":
    main()
