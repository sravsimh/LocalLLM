import subprocess
import json
import time
import argparse
import os
import csv
import requests


def run_and_store_final_response(model, url="http://127.0.0.1:11434/api/generate"):
    try:
        # Prepare the payload
        payload = {
            "model": model,
            "prompt": "What is AI?"
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Run the request and time it
        start_time = time.time()
        response = requests.post(url, headers=headers,
                                 json=payload, stream=True)
        end_time = time.time()

        if not response.ok:

            if (response.status_code) == 404:
                print("Download error, Re-Downloading Weights")
                subprocess.run(["ollama", "pull", model])
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
        tpm = total_tokens / eval_duration if eval_duration > 0 else 0
        latency = end_time - start_time

        metrics = {
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

        write_metrics_to_csv(model, metrics)

        exit(0)

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        exit(1)
    except Exception as e:
        print("Unexpected error:", e)
        exit(1)


def write_metrics_to_csv(model_id, metrics, csv_file="benchmark_results.csv"):
    fieldnames = ["runs_id", "model_id"] + list(metrics.keys())

    runs_id = 1
    if os.path.isfile(csv_file):
        with open(csv_file, mode='r', newline='') as file:
            runs_id = len((list(csv.reader(file))))

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if os.path.getsize(csv_file) == 0:
            writer.writeheader()

        row = {"runs_id": runs_id, "model_id": model_id}
        row.update(metrics)
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Run benchmark with model")
    parser.add_argument("--model", required=True,
                        help="Model name to benchmark (llama3.1:8b, gemma2:2b, qwen2.5:7b)")
    args = parser.parse_args()
    run_and_store_final_response(args.model)


if __name__ == "__main__":
    main()
