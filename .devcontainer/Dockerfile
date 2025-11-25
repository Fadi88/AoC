
FROM ubuntu:24.04
FROM rust:1.72

ENV TZ="Europe/Berlin"

RUN apt update && \
    apt install -y git python3 cmake curl python3-pip && \
    pip install advent-of-code-data
