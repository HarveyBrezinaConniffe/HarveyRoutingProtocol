from collections import namedtuple
import socket
import Packets
from math import inf

PORT = 54321

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

Link = namedtuple("Link", ["destIP", "destName"])

# Graph of network topology as an adjacency list 
topology = {
    "FF:00:00": [Link("172.17.17.1", "FF:00:01")],
    "FF:00:01": [Link("172.17.17.0", "FF:00:00"), Link("172.17.18.1", "FF:00:02")],
    "FF:00:02": [Link("172.17.18.0", "FF:00:01")]
}

def shortestPaths(topologyGraph, source):
  unfinalized = []
  distances = {}

  for node in topologyGraph:
    distances[node] = inf
    unfinalized.append(node)

  distances[source] = 0
  current = source

  while len(unfinalized) > 1:
    for link in topologyGraph[current]:
      distances[link.destName] = min(distances[link.destName], distances[current]+1)
    unfinalized.remove(current)

    minDist = distances[unfinalized[0]]
    minNode = unfinalized[0]
    for node in unfinalized:
      if distances[node] < minDist:
        minDist = distances[node]
        minNode = node
    current = minNode
  
  return distances
    

def recievePacket(data, addr):
  packet = Packets.decodePacket(data)
  if packet == None:
    return
  if packet.type == Packets.typeToNum["Hello"]:
    print("Recieving hello from {}".format(packet.routerIP))
    nextHop = routingTable[packet.routerIP]
    response = Packets.NextHopPacket(routingTable[packet.routerIP]).encode()
    print("Replying to {}".format(addr[0]))
    sock.sendto(response, (addr[0], PORT))

if __name__ == "main":
  while True:
    data, addr = sock.recvfrom(512)
    recievePacket(data, addr)
