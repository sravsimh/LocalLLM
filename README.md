## Note

This project is still under developement, kindly raise issues if you run into anything.

# LLM Benchmarking
This project is to create a benchmark software to run on a loacal machine to benchmark the performance of a 3 LLM's  Llama 3.1 8B, Qwen 2.5, Gemma 2B and determine if it is beneficial to run locally or to infer over cloud.

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

If there are no errors you should get something like:
```text
data is in json file and logs are in ollama_debug.log
```

