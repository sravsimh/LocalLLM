import subprocess
import json
import time
import argparse
import os
import csv
import requests
import psutil


avg_eval_time = 0
avg_prompt_eval_duration = 0
avg_total_time = 0
avg_load_time = 0
avg_tmp = 0
avg_latency = 0

OLLAMA_LOG = "ollama_debug.log"


def stop_ollama_server():

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'ollama' in proc.info['name'].lower():
                proc.terminate()
                proc.wait(timeout=5)
        except Exception as e:
            print("Error stopping ollama:", e)
            exit(1)


def start_ollama():
    print("starting server")
    cmd_serve = ["ollama", "serve"]
    with open(OLLAMA_LOG, "w", encoding="utf-8") as log_file:
        if os.name == "posix":
            # Prepare the payload
            print("running a different model to remove ollama from memory")
            payload = {
                "model": "smollm2:135m",
                "prompt": "heyloooo",
                "keep_alive": 0,
            }

            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(
                "http://127.0.0.1:11434/api/generate", headers=headers, json=payload, stream=False)
        else:
            PORT = 11434

            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == PORT:
                    pid = conn.pid
                    try:
                        proc = psutil.Process(pid)

                        proc.terminate()  # Send SIGTERM
                        proc.wait(timeout=5)  # Wait for process to exit
                    except Exception as e:
                        print(e)

                    break
        try:
            process = subprocess.Popen(
                cmd_serve,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                env=os.environ
            )

        except Exception as e:
            print(f"Error starting Ollama server: {e}")
            exit(1)


def load_model(model):
    print(f"loading model {model}...")
    headers = {
        "Content-Type": "application/json"
    }
    requests.post("http://127.0.0.1:11434/api/generate",
                  headers=headers, json={"model": model})


def unload_model(model):
    print(f"Unloading model {model}...")
    headers = {
        "Content-Type": "application/json"
    }
    requests.post("http://127.0.0.1:11434/api/generate",
                  headers=headers, json={"model": model, "keep_alive": 0})


def run_and_store_final_response(model, prompt, i, url="http://127.0.0.1:11434/api/generate"):
    global avg_load_time, avg_total_time, avg_eval_time, avg_latency, avg_prompt_eval_duration, avg_tmp

    try:

        start_ollama()
        load_model(model)

        # Prepare the payload
        payload = {
            "model": model,
            "prompt": prompt,
            "keep_alive": 0,
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Run the request and time it
        start_time = time.time()
        response = requests.post(url, headers=headers,
                                 json=payload, stream=False)
        end_time = time.time()
        print(f"benchmarking model with {i+1} st/nd/rd promt")
        unload_model(model)
        if not os.name == "posix":
            stop_ollama_server()
        if not response.ok:

            if (response.status_code) == 404:
                print("Download error, Re-Downloading Weights")
                subprocess.run(["ollama", "pull", model])
                start_time = time.time()
                response = requests.post(url, headers=headers,
                                         json=payload, stream=False)
                end_time = time.time()

            else:
                print(
                    f"Error from API: {response.status_code} - {response.text}")
                exit(1)
        # Parse the streamed response: get the last full JSON line
        last_json = None
        for line in response.iter_lines():
            if not line:
                continue
            try:
                decoded = line.decode('utf-8').strip()
                if decoded.startswith("{"):
                    last_json = json.loads(decoded)
            except Exception:
                continue
        if last_json is None:
            print("No valid JSON response received.")
            exit(1)

        # Extract metrics
        total_duration = last_json['total_duration'] / 1e9
        load_duration = last_json['load_duration'] / 1e9
        prompt_eval_duration = last_json['prompt_eval_duration'] / 1e9
        eval_duration = last_json['eval_duration'] / 1e9
        prompt_count = last_json['prompt_eval_count']
        eval_count = last_json['eval_count']
        total_tokens = prompt_count + eval_count
        tpm = (total_tokens / prompt_eval_duration + eval_duration) * \
            60 if eval_duration > 0 else 0
        latency = end_time - start_time
        if (latency < 0):
            print(end_time, start_time, "latency is -ve")
            exit(1)

        metrics = {
            "prompt-id": i,
            "total_duration": round(total_duration, 2),
            "load_duration": round(load_duration, 2),
            "prompt_eval_duration": round(prompt_eval_duration, 2),
            "eval_duration": round(eval_duration, 2),
            "prompt_count": prompt_count,
            "eval_count": eval_count,
            "total_tokens": total_tokens,
            "tpm": round(tpm, 2),
            "latency": round(latency, 2)
        }
        avg_eval_time += round(eval_duration, 2)
        avg_prompt_eval_duration += round(prompt_eval_duration, 2)
        avg_total_time += round(total_duration, 2)
        avg_load_time += round(load_duration, 2)
        avg_tmp += round(tpm, 2)
        avg_latency += round(latency, 2)

        write_metrics_to_csv(model, metrics, "benchmark_results.csv")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        exit(1)
    except Exception as e:
        print("Unexpected error:", e)
        exit(1)


def write_metrics_to_csv(model_id, metrics, csv_file):
    fieldnames = ["runs", "model_id"] + list(metrics.keys())

    runs_id = 1
    if os.path.isfile(csv_file):
        with open(csv_file, mode='r', newline='') as file:
            runs_id = len((list(csv.reader(file))))

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if os.path.getsize(csv_file) == 0:
            writer.writeheader()

        row = {"runs": runs_id, "model_id": model_id}
        row.update(metrics)
        writer.writerow(row)


def main():

    parser = argparse.ArgumentParser(description="Run benchmark with model")
    parser.add_argument("--model", required=True,
                        help="Model name to benchmark (llama3.1:8b, gemma2:2b, qwen2.5:7b)")
    args = parser.parse_args()
    prompts = [
        "Hello who are",
        "Can you tell me about Shram.ai from banglore?",
        "what is 12165551231321512232321*1527132612836871263/23354351321354854313+546842165465132184320"
    ]
    for i, p in enumerate(prompts):
        run_and_store_final_response(args.model, p, i)

    metrics = {

        "avg_total_time": round(avg_total_time/3, 2),
        "avg_load_time": round(avg_load_time/3, 2),
        "avg_prompt_eval_duration": round(avg_prompt_eval_duration/3, 2),
        "avg_eval_time": round(avg_eval_time/3, 2),
        "avg_tmp": round(avg_tmp/3, 2),
        "avg_latency": round(avg_latency/3, 2)
    }
    write_metrics_to_csv(args.model, metrics, "Avg_benchmark_results.csv")


if __name__ == "__main__":
    main()
