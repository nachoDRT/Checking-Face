FROM nvidia/cuda:11.0.3-base-ubuntu20.04

# Desactivar la interacción durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Agregar el repositorio de deadsnakes para instalar Python 3.10
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update

# Instalar Python 3.10 y paquetes relacionados
RUN apt-get install -y \
    python3.10 \
    python3.10-distutils \
    libjpeg-dev \
    zlib1g-dev \
    git \
    curl

# Configurar Python 3.10 como el python3 por defecto
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1


RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.10 get-pip.py && \
    rm get-pip.py

RUN python3.10 -m pip install --upgrade pip setuptools wheel
# Crear el directorio de trabajo
WORKDIR /app

# Instalar PyTorch (versión compatible con CUDA 11.1)  
RUN pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html

# Copiar e instalar los requerimientos
COPY dockerfiles/rtx3090/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Configurar variables de entorno (reemplazar <your_access_token> por el token real)
ENV WANDB_API_KEY=<your_access_token>
ENV HUGGINGFACE_HUB_TOKEN=<your_access_token>

# Ejecutar el script de inicio
RUN chmod +x src/start.sh
CMD ["bash", "src/start.sh"]
