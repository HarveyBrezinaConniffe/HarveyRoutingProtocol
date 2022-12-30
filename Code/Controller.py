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
    "ff:00:00": [Link("172.20.17.11", "ff:00:01")],
    "ff:00:01": [Link("172.20.17.10", "ff:00:00"), Link("172.20.18.11", "ff:00:02")],
    "ff:00:02": [Link("172.20.18.10", "ff:00:01")]
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
  if packet.type == Packets.typeToNum["RequestInfo"]:  
    print("Forwarder {} requesting nextHop for {}".format(packet.forwarderName, packet.dest))
    distances = shortestPaths(topology, packet.dest)
    closestDistance = inf
    closestIP = None
    for link in topology[packet.forwarderName]:
      if distances[link.destName] < closestDistance:
        closestDistance = distances[link.destName]
        closestIP = link.destIP
    print("Closest hop is {}".format(closestIP))
    responsePacket = Packets.NextHopPacket(packet.dest, closestIP)
    sock.sendto(responsePacket.encode(), (addr[0], PORT))
  if packet.type == Packets.typeToNum["AddService"]:
    print("New Service")
    topology[packet.forwarderName].append(Link("-1", packet.name))
    topology[packet.name] = [Link("-1", packet.forwarderName)]

while True:
  data, addr = sock.recvfrom(512)
  recievePacket(data, addr)
