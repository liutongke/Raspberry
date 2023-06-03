#!/bin/bash

data_dir="./data"

if [ ! -d "$data_dir" ]; then
    echo "Creating data directory..."
    mkdir "$data_dir"
    echo "Data directory created."
else
    echo "Data directory already exists."
fi

sudo docker build -t monitor-nvr-process-python:v1 .
sudo docker run --name monitor-nvr-process-python-server -itd -p 9090:9090/udp -v $data_dir:/var/www/html/data monitor-nvr-process-python:v1