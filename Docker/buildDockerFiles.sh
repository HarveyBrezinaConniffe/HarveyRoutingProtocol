#!/bin/zsh
docker build -t forwarderimage ./Forwarder
docker build -t clientimage ./Client
docker build -t serverimage ./Server
