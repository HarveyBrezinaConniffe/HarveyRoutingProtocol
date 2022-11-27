import socket
import Packets

PORT = 54321

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nearestNode = input("Nearest forwarder> ")

dest = input("Message destination> ")
payload = input("Message payload> ")

packet = Packets.MessagePacket(dest, payload.encode("utf-8"))
sock.sendto(packet.encode(), (nearestNode, PORT))
