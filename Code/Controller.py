import socket
import Packets

PORT = 54321

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

routingTable = {"172.41.0.2": "172.41.0.3", "172.42.0.2": "172.42.0.3", "172.43.0.3": "172.43.0.2"}

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
