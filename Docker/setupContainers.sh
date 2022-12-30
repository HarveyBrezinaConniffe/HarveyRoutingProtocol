#!/bin/zsh
docker network create -d bridge --subnet 172.20.20.0/24 homeNetwork
docker network create -d bridge --subnet 172.20.17.0/24 internalNetwork1
docker network create -d bridge --subnet 172.20.18.0/24 internalNetwork2
docker network create -d bridge --subnet 172.20.19.0/24 cloudProviderNetwork
docker network create -d bridge --subnet 172.25.0.0/24 controllerNetwork

docker create -ti --name controller --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code controllerimage /bin/bash

docker create -ti --name client --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code clientimage /bin/bash

docker create -ti --name server --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code serverimage /bin/bash

docker create -ti --name forwarder1 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash
docker create -ti --name forwarder2 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash
docker create -ti --name forwarder3 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash

docker network connect --ip 172.25.0.10 controllerNetwork controller
docker network connect --ip 172.25.0.11 controllerNetwork forwarder1
docker network connect --ip 172.25.0.12 controllerNetwork forwarder2
docker network connect --ip 172.25.0.13 controllerNetwork forwarder3

docker network connect --ip 172.20.20.10 homeNetwork client
docker network connect --ip 172.20.20.11 homeNetwork forwarder1

docker network connect --ip 172.20.17.10 internalNetwork1 forwarder1
docker network connect --ip 172.20.17.11 internalNetwork1 forwarder2

docker network connect --ip 172.20.18.10 internalNetwork2 forwarder2
docker network connect --ip 172.20.18.11 internalNetwork2 forwarder3

docker network connect --ip 172.20.19.10 cloudProviderNetwork forwarder3
docker network connect --ip 172.20.19.11 cloudProviderNetwork server

docker start controller
docker start client
docker start server
docker start forwarder1
docker start forwarder2
docker start forwarder3
