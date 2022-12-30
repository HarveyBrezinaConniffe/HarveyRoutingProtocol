from collections import namedtuple
import socket
import Packets

PORT = 54321

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

Link = namedtuple("Link", ["destIP", "destName"])

# Graph of network topology as an adjacency list 
topology = {
    "FF:00:00": [Link("172.17.17.1", "FF:00:01")],
    "FF:00:01": [Link("172.17.17.0", "FF:00:00"), Link("172.17.18.1", "FF:00:02")],
    "FF:00:02": [Link("172.17.18.0", "FF:00:01"), Link("172.17.19.1", "FF:00:03")],
    "FF:00:03": [Link("172.17.19.0", "FF:00:02")]
}

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

while True:
  data, addr = sock.recvfrom(512)
  recievePacket(data, addr)
