#!/bin/zsh
docker stop client
docker stop server
docker stop forwarder1
docker stop forwarder2
docker stop forwarder3
docker stop controller

docker network remove homeNetwork
docker network remove ispNetwork
docker network remove publicNetwork
docker network remove cloudProviderNetwork
docker network remove controllerNetwork

docker rm client
docker rm server
docker rm forwarder1
docker rm forwarder2
docker rm forwarder3
docker rm controller
