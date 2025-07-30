## Note
This project is still under developement, kindly raise issues if you run into anything.

# Issues
When running in linux or unix the server cant be stopped with psutil and requires sudo, to overcome this i have come up with a solution:
>running a small model between two benchmarking runs ([smollm2:135m](https://ollama.com/library/smollm2)) this removes the model from Memory and ram resulting in accurate benchmark timings.

# LLM Benchmarking
This Repository aims to create a software to run on a loacal machine to benchmark the performance of LLM's like Llama 3.1 8B, Qwen 2.5, Gemma 2B and determine if it is beneficial to run locally.

This repository is using Ollama library for local LLM setup since it is user-friendly and easy to setup

>**Note** this repository only tests 4 Bit Quantized models from Ollama libraby

# System Requirements

The Minimum System Requirements are:<br>
CPU - intel i5 or greater<br>
RAM - 6GB or Higher<br>
VRAM - 2GB or Higher<br>
GPU - 2GB or Higher(for larger models)<br>
Disk Space - 5 - 15 GiB (Higer for larger models)<br>

To Check system requirements of any model visit [ApXML](https://apxml.com/models), in the Quantization field please select INT4 / Ollama

>**Note**
While selecting the models please select only recommended models for better performance


# Setup
This project setup requires installing [Ollama](https://ollama.com/) a free software to easily run LLM's Locally

To check if ollama is installed run:
```bash
ollama --version
```

Now clone this repository by running:<br>
```bash
git clone https://github.com/sravsimh/LocalLLM.git
```
Once ollama is installed and you cloned this repository, create a virtual environment using [conda](https://www.anaconda.com/docs/getting-started/miniconda/main) 
```bash
conda create -n your-env-name python=3.11
```

Once env is activated run the following:
```python
pip install -r requirements.txt
python main.py
```
Currently its supports only models included below:<br>
<br>
Gemma 2B <br>
Gemma 7B <br>
LLaMA 3.1 8B <br>
Qwen 2.5 0.5B <br>
Qwen 2.5 1.5B <br>
Qwen 2.5 3B <br>
Qwen 2.5 7B <br>

If you want to test any other model supported by ollama,<br>
First pull the weights:
```bash
ollama pull modelName
```

then, try:
```bash
python main.py --model modelName
```
# Results
To view results, there are 4 files:
>Avg_benchmark_results.csv for AVG of 3 prompt Benchmarks<br>
>benchmark_results.csv for benchmarks of each run<br>
>stats.json for your pc specifications<br>
>ollama_debug.log for loggs of the server(suggested for developers)<br>

Based on these things we can decide if its beneficial to run locally.

| Model (size)             | Acceptable TPM | Good TPM     | Excellent TPM |
| ------------------------ | -------------- | ------------ | ------------- |
| **Small (1B–3B)**        | 3,000–6,000    | 6,000–10,000 | >10,000       |
| **Medium (7B)**          | 1,500–3,000    | 3,000–5,000  | >5,000        |
| **Large (13B)**          | 800–2,000      | 2,000–3,500  | >3,500        |
| **Very Large (30B–65B)** | 200–1,000      | 1,000–2,000  | >2,000        |



<p align="center">Made with ❤️ by <strong>Sravsimh</strong></p>


