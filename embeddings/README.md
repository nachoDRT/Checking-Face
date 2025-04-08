# Nvidia RTX2080/3090/4090
Execute from ./checking-face/embeddings

Available cards: `RTX2080`, `RTX3090`, `RTX4090`

### Create the docker :whale:
```bash
docker build -f dockerfiles/your_card/Dockerfile -t checking-face .
```

### Run :boom: or Debug :no_entry_sign::bug: the docker
```bash
docker run -it --gpus '"device=0"' --ipc=host checking-face
```

```bash
docker run -p 5678:5678 -it --gpus '"device=0"' --ipc=host checking-face
```

### Inspect default dataset using a volume
```bash
docker run -v /host_path_to_save_dataset_inspection:/app/dataset_inspection checking-face
```