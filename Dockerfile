FROM ubuntu:24.04

RUN \
    DEBIAN_FRONTEND=noninteractive \
    apt update && \
    DEBIAN_FRONTEND=noninteractive \
    apt install -y \
    build-essential \
    git \
    inkscape \
    libcairo2-dev \
    libpango1.0-dev \
    libpixman-1-dev \
    nodejs \
    npm \
    pandoc \
    pkg-config \
    python3 \
    python3-pip \
    texlive \
    wget && \
    DEBIAN_FRONTEND=noninteractive \
    rm -rf /var/lib/apt/lists/*

RUN \
    python3 -m pip install --no-cache-dir --break-system-packages \
    beautifulsoup4==4.12.3 \
    matplotlib==3.8 \
    python-docx==1.1 \
    requests==2.31 \
    ruff==0.4

RUN \
    npm install -g \
    @mermaid-js/mermaid-cli@10.9 \
    @penrose/roger@3.2

COPY ./ /docx-202405-from-md

ENTRYPOINT ["bash", "/docx-202405-from-md/build.sh"]

CMD []
