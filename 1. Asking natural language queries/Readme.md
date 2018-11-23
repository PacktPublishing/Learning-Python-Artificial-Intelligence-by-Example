# Asking Natural Language Queries

This repo contains the code for the "Learning Python by Example" module for asking natural language queries.

## Getting started

First, install Docker for your laptop or server (see https://docs.docker.com/install/), then enter the following commands (note that Windows commands may be different):

```bash
cd Docker
docker build --tag python-ai-1:1 .
```
Note that this will run for a while as packages such as Anaconda are installed.

Once the build process has finished, you can run the container using:

```bash
docker run -di -v <path_to_this_dir>/Source:/root/source --name "python-ai-1" python-ai-1:1 /bin/bash
```

and then you can connect to the container using

```bash
docker exec -ti python-ai-1 bash
```


Example `curl` command:

```curl -H "Content-Type: application/json" -X POST localhost:5000/lda --data '{"query": "using deep learning for computer vision in real time"}'```
