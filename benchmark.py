import subprocess
import json
import time
import argparse
import os
import csv

from main import run_benchmark


def run_and_store_final_response(model, command):
    try:
        # Run the command
        start_time = time.time()
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)
        end_time = time.time()
        jsonvalue = json.loads(result.stdout.split('\n')[-2])
        jsonvalue.pop('context', None)

        try:
            # Write the output to a file
            with open('final_response.json', 'w') as f:
                json.dump({"response": jsonvalue}, f, indent=4)

            total_duration = (jsonvalue['total_duration'])/1e9
            load_duration = (jsonvalue['load_duration'])/1e9
            prompt_eval_duration = (jsonvalue['prompt_eval_duration'])/1e9
            eval_duration = (jsonvalue['eval_duration'])/1e9
            prompt_count = jsonvalue['prompt_eval_count']
            eval_count = jsonvalue['eval_count']
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

        except IOError as io_error:
            print("Error writing to file:", io_error)
            exit(1)
    except Exception as e:
        print(" Error running command:", e)
        exit(1)


def write_metrics_to_csv(model_id, metrics, csv_file="benchmark_results.csv"):
    fieldnames = ["runs_id", "model_id"] + list(metrics.keys())

    runs_id = 1
    if os.path.isfile(csv_file):
        with open(csv_file, mode='r', newline='') as file:
            # includes header, so it works as run_id
            runs_id = len((list(csv.reader(file))))

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header if file is empty
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
    cmd = (
        f'curl http://127.0.0.1:11434/api/generate '
        '-H "Content-Type: application/json" '
        f'-d "{{\\"model\\": \\"{args.model}\\", \\"prompt\\": \\"What is AI?\\"}}"'
    )

    run_and_store_final_response(args.model, cmd)


if __name__ == "__main__":
    main()
