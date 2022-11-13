import socket
import Packets

PORT = 54321

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))
sock.settimeout(3)

# Map dest ID to next node IP
forwardingTable = {}

while True:
	inp = input("Forwarding table entry> ")
	if inp == "":
		break
	destID, nextHop = inp.split(" ")
	forwardingTable[destID.lower()] = nextHop

def recievePacket(data, addr):
	packet = Packets.decodePacket(data)
	if packet == None:
		return

	if packet.type == Packets.typeToNum["MessagePacket"]:
		print("Recieving packet destined for {} with payload {}".format(packet.dest, packet.payload))
		nextHop = forwardingTable[packet.dest.lower()]
		print("Next hop is {}".format(nextHop))
		sock.sendto(data, (nextHop, PORT))

while True:
	try:
		data, addr = sock.recvfrom(512)
		recievePacket(data, addr)
	except:
		pass
