#!/bin/zsh
docker network create -d bridge --subnet 172.17.20.0/24 homeNetwork
docker network create -d bridge --subnet 172.17.17.0/24 internalNetwork1
docker network create -d bridge --subnet 172.17.18.0/24 internalNetwork2
docker network create -d bridge --subnet 172.17.19.0/24 cloudProviderNetwork
docker network create -d bridge --subnet 172.50.0.0/24 controllerNetwork

docker create -ti --name controller --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code controllerimage /bin/bash

docker create -ti --name client --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code clientimage /bin/bash

docker create -ti --name server --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code serverimage /bin/bash

docker create -ti --name forwarder1 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash
docker create -ti --name forwarder2 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash
docker create -ti --name forwarder3 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash

docker network connect --ip 172.50.0.0 controllerNetwork controller
docker network connect controllerNetwork forwarder1
docker network connect controllerNetwork forwarder2
docker network connect controllerNetwork forwarder3

docker network connect --ip 172.17.20.0 homeNetwork client
docker network connect --ip 172.17.20.1 homeNetwork forwarder1

docker network connect --ip 172.17.17.0 internalNetwork1 forwarder1
docker network connect --ip 172.17.17.1 internalNetwork1 forwarder2

docker network connect --ip 172.17.18.0 internalNetwork2 forwarder2
docker network connect --ip 172.17.18.1 internalNetwork2 forwarder3

docker network connect --ip 172.17.19.0 cloudProviderNetwork forwarder3
docker network connect --ip 172.17.19.1 cloudProviderNetwork server

docker start controller
docker start client
docker start server
docker start forwarder1
docker start forwarder2
docker start forwarder3
