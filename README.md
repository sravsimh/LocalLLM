## Note

This project is still under developement, kindly raise issues if you run into anything.

# LLM Benchmarking
This project is to create a benchmark software to run on a loacal machine to benchmark the performance of a 3 LLM's  Llama 3.1 8B, Qwen 2.5, Gemma 2B and determine if it is beneficial to run locally or to infer over cloud.

# System Requirements

The Minimum System Requirements are:<br>
CPU - intel i5 or greater<br>
RAM - 6GB or Higher<br>
VRAM - 2GB or Higher<br>
GPU - 2GB or Higher(for larger models)<br>
Disk Space - 5 - 15 GiB (Higer for larger models)<br>

>**Note**
While selecting the models please select only recommended models for better performance


# Setup
This project setup requires installing [Ollama](https://ollama.com/) a free software to easily run LLM's Locally

To check if ollama is installed run:
```bash
ollama --version
```

Once ollama is installed, then clone this repository and create a virtual environment using [conda](https://www.anaconda.com/docs/getting-started/miniconda/main) 
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
gemma:2b: Gemma 2B (No GPU)<br>
gemma:7b: Gemma 7B (GPU)<br>
llama3.1:8b: LLaMA 3.1 8B (GPU)<br>
qwen2.5:0.5b: Qwen 2.5 0.5B (No GPU)<br>
qwen2.5:1.5b: Qwen 2.5 1.5B (No GPU)<br>
qwen2.5:3b: Qwen 2.5 3B (No GPU)<br>
qwen2.5:7b: Qwen 2.5 7B (GPU)<br>

If you want to test any other model supported by ollama,<br>
First pull the weights:
```bash
ollama pull modelName
```

then, try:
```bash
python main.py --model modelName
```

<p align="center">Made with ❤️ by <strong>Sravsimh</strong></p>


