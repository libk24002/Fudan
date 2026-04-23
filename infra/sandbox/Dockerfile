FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ openjdk-21-jdk-headless time \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 sandbox

USER sandbox
WORKDIR /workspace
