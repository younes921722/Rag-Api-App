# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.8 or later

#### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

<!-- ### Install Ollama (Optional)

1) Install Ollama from [here](https://github.com/ollama/ollama/tree/main#ollama)
2) Pull one of the models from [here](https://github.com/ollama/ollama/tree/main#model-library)

```bash
$ ollama pull dolphin-phi
```

3) (**Optional**) set the `OLLAMA_HOST` in your operating system to be `0.0.0.0`
4) Run the Ollama server 

```bash

$ ollama serve

``` -->

5) (**Optional**) Explore the APIs [Docs](https://github.com/ollama/ollama/blob/main/docs/api.md)


## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection

Download the POSTMAN collection from [/assets/mini-rag-dev.postman_collection.json](/assets/mini-rag-dev.postman_collection.json)

## API Docs

- Swagger UI: http://localhost:5000/docs

## APIs

### 1) Upload a document

```bash
curl --location --request POST 'http://localhost:5000/api/v1/upload/1' \
--form 'file=@"/C:/Users/Home/Desktop/wiki.txt"'
```
