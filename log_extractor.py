import re
import json
import os
import sys

log_path = os.path.join(os.getcwd(), "ollama_debug.log")
output_json = os.path.join(os.getcwd(), "Detailed_benchmark.json")

# Ensure the log file exists
if not os.path.isfile(log_path):
    print(f"Log file not found: {log_path}")
    sys.exit(1)

# Load log content
with open(log_path, "r", encoding="utf-8") as f:
    logs = f.read()

# Regex patterns to extract from logs
patterns = {
    "model_name": r"registry\.ollama\.ai/library/([^\s]+)",
    "vram": r"runner\.vram=\"([\d\.]+ GiB)\"",
    "model_size": r"runner\.size=\"([\d\.]+ GiB)\"",
    "devices": r"runner\.devices=([^\s]+)",
    "inference_type": r"runner\.inference=([^\s]+)",
    "context_size": r"runner\.num_ctx=(\d+)",
    "kv_buffer_cuda": r"CUDA0 KV buffer size =\s+([\d\.]+ MiB)",
    "kv_buffer_cpu": r"CPU KV buffer size =\s+([\d\.]+ MiB)",
    "kv_self_size": r"KV self size\s+=\s+([\d\.]+ MiB)",
    "cuda_compute_buffer": r"CUDA0 compute buffer size =\s+([\d\.]+ MiB)",
    "cuda_host_buffer": r"CUDA_Host compute buffer size =\s+([\d\.]+ MiB)",
    "graph_nodes": r"graph nodes\s+=\s+(\d+)",
    "graph_splits_bs512": r"graph splits = (\d+) \(with bs=512\)",
    "graph_splits_bs1": r"graph splits = \d+ \(with bs=512\), (\d+) \(with bs=1\)",
    "model_path": r"runner\.model=([^\s]+)",
    "startup_time": r"ollama runner started in ([\d\.]+ seconds)",
    "completion_time": r"\|\s+(\d+m\d+s)\s+\|\s+127\.0\.0\.1\s+\|\s+POST\s+\"/api/generate\""

}

# Extract latest value per pattern
results = {}
for key, pattern in patterns.items():
    matches = re.findall(pattern, logs)
    results[key] = matches[-1] if matches else None

if os.path.exists(output_json):
    with open(output_json, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# Append the new result
data.append(results)

# Save the updated list back to the file
with open(output_json, "w", encoding="utf-8") as out_f:
    json.dump(data, out_f, indent=4)
