FROM rust:1-bookworm

ENV TZ="Europe/Berlin"

RUN apt-get update && \
    apt-get install -y --no-install-recommends git python3 python3-pip python3-venv cmake g++ && \
    rm -rf /var/lib/apt/lists/*

RUN rustup component add clippy rustfmt
