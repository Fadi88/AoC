
FROM ubuntu:latest

RUN apt update && \
    apt install -y git python3 cmake curl

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
ENV TZ="Europe/Berlin"
