#!/usr/bin/env bash

set -e

pip install poetry --user && poetry update

sudo apt update
sudo apt install -y cargo
cargo install st-cli
