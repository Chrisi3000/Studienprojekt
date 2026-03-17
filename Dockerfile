FROM python:3.10

RUN apt-get update && apt-get install -y \
    samtools \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install "numpy<2"
RUN pip install .

CMD ["bash"]