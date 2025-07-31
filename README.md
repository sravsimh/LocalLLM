## Note
This project is still under developement, kindly raise issues if you run into anything.

# Common Issues

If you get a request Error or Error in benchmarks script these might be the possible reasons:
>You are running multiple ollama instances so quit ollama from taskbar<br>
>Or, You configured your Ollama to run on a different port so either switch back to 11434 or in benchmar.py change the port 11434 to your port.<br>
>If you are running with --model then either the model is not pulled or you are spelling the modelName wrong

If you run into any other issues in benchmark.py please raise issues with details.

When running in linux or unix the server can't be stopped with psutil and requires sudo, to overcome this I have come up with a solution:
>running a small model between two benchmarking runs ([smollm2:135m](https://ollama.com/library/smollm2)) this removes the main model from Memory and RAM resulting in accurate benchmark timings.






# LLM Benchmarking
This Repository aims to create a software to run on a loacal machine to benchmark the performance of LLM's like Llama 3.1 8B, Qwen 2.5, Gemma 2B and determine if it is beneficial to run locally.

This repository is using Ollama library for local LLM setup since it is user-friendly and easy to setup

>**Note** this repository only tests 4 Bit Quantized models from Ollama library

# System Requirements

The Minimum System Requirements are:<br>
CPU - intel i5 or greater<br>
RAM - 6GB or Higher<br>
VRAM - 2GB or Higher<br>
GPU - 2GB or Higher(for larger models)<br>
Disk Space - 5 - 15 GiB (Higher for larger models)<br>

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
Now, create virtual environment using [conda](https://www.anaconda.com/docs/getting-started/miniconda/main) 
```bash
conda create -n envs-name python=3.11
```

Once env is activated run the following:
```python
pip install -r requirements.txt
python main.py
```
Currently it supports only models included below:<br>
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
>ollama_debug.log for logs of the server(recommended for developers)<br>

Based on this we can decide if its beneficial to run locally.

Refer to below table for referance:

| Model-(size of parameters)| Minimum TPM    | Good   TPM   | Excellent TPM |
| ------------------------  | -------------- | ------------ | ------------- |
| **small (1B–3B)**         | 3,000–6,000    | 6,000–10,000 | >10,000       |
| **medium (7B)**           | 1,500–3,000    | 3,000–5,000  | >5,000        |
| **large (13B)**           | 800–2,000      | 2,000–3,500  | >3,500        |


# Extension
If you have a good hardware with GPU > 16 GB you can try the 16 bit models which have higher precision(accurate answers), Make sure you have atleast 20GiB of storage
```bash
python main.py --model qwen2.5:1.5b-instruct-fp16
python main.py --model qwen2.5:3b-instruct-fp16
python main.py --model gemma:2b-instruct-fp16
```


<p align="center">made with ❤️ by --<strong>sravsimh</strong>--</p>


