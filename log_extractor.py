import re
import json

log_path = "ollama_debug.log"
output_json = "llama_benchmark.json"

# Load log
with open(log_path, "r", encoding="utf-8") as f:
    logs = f.read()

# Patterns to extract add any if you want to monitor more
patterns = {
    "vram": r"runner\.vram=\"([\d\.]+ GiB)\"",  # gives vram usage
    "model_size": r"runner\.size=\"([\d\.]+ GiB)\"",  # gives model size
    "devices": r"runner\.devices=([^\s]+)",  # gives devices used
    # gives inference type
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
    "startup_time": r"llama runner started in ([\d\.]+ seconds)",
    "completion_time": r"\|\s+(\d+m\d+s)\s+\|\s+127.0.0.1\s+\|\s+POST\s+\"/api/generate\""
}

results = {}
for key, pattern in patterns.items():
    matches = re.findall(pattern, logs)
    if matches:
        last_value = matches[-1]
        results[key] = last_value
    else:
        results[key] = None  # or handle missing values as needed


# Save as JSON
with open(output_json, "w") as out_f:
    json.dump(results, out_f, indent=4)

print("Extracted metrics saved to", output_json)
