#!/bin/zsh
docker stop client
docker stop server
docker stop forwarder1
docker stop forwarder2
docker stop forwarder3
docker stop controller

docker network remove homeNetwork
docker network remove internalNetwork1
docker network remove internalNetwork2
docker network remove cloudProviderNetwork
docker network remove controllerNetwork

docker rm client
docker rm server
docker rm forwarder1
docker rm forwarder2
docker rm forwarder3
docker rm controller
