#!/bin/zsh
docker network create -d bridge --subnet 172.40.0.0/16 homeNetwork
docker network create -d bridge --subnet 172.41.0.0/16 ispNetwork
docker network create -d bridge --subnet 172.42.0.0/16 publicNetwork
docker network create -d bridge --subnet 172.43.0.0/16 cloudProviderNetwork
docker network create -d bridge --subnet 172.50.0.0/16 controllerNetwork

docker create -ti --name controller --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code controllerimage /bin/bash

docker create -ti --name client --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code clientimage /bin/bash

docker create -ti --name server --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code serverimage /bin/bash

docker create -ti --name forwarder1 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash
docker create -ti --name forwarder2 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash
docker create -ti --name forwarder3 --cap-add=all -v /Users/harvey/HarveyRoutingProtocol/Code:/home/Code forwarderimage /bin/bash


docker network connect controllerNetwork controller
docker network connect controllerNetwork forwarder1
docker network connect controllerNetwork forwarder2
docker network connect controllerNetwork forwarder3

docker network connect homeNetwork client
docker network connect homeNetwork forwarder1

docker network connect ispNetwork forwarder1
docker network connect ispNetwork forwarder2

docker network connect publicNetwork forwarder2
docker network connect publicNetwork forwarder3

docker network connect cloudProviderNetwork forwarder3
docker network connect cloudProviderNetwork server

docker start controller
docker start client
docker start server
docker start forwarder1
docker start forwarder2
docker start forwarder3
