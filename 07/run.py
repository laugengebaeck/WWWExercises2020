import argparse
import random
import socket, struct
import array

# TCP flag constants
TCP_FLAGS_RSV = (0 << 9)
TCP_FLAGS_NOC = (0 << 8)
TCP_FLAGS_CWR = (0 << 7)
TCP_FLAGS_ECN = (0 << 6)
TCP_FLAGS_URG = (0 << 5)
TCP_FLAGS_ACK = (0 << 4)
TCP_FLAGS_PSH = (0 << 3)
TCP_FLAGS_RST = (0 << 2)
TCP_FLAGS_SYN = (1 << 1)
TCP_FLAGS_FIN = (0)

# source: https://github.com/secdev/scapy/blob/master/scapy/utils.py
def chksum(packet):
    if len(packet) % 2 != 0:
        packet += b'\0'

    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16

    return (~res) & 0xffff

class TCPPacket:
    def __init__(self, src_ip, src_port, dst_ip, dst_port, data, flags, seqnum = 0, acknum = 0):
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.data = data
        self.flags = flags
        self.seqnum = seqnum
        self.acknum = acknum

    def build(self):
        packet = struct.pack(
            '!HHIIBBHHH',
            self.src_port,  # Source Port
            self.dst_port,  # Destination Port
            self.seqnum,    # Sequence Number
            self.acknum,    # Acknoledgement Number
            5 << 4,         # Data Offset
            self.flags,     # Flags
            8192,           # Window
            0,              # Checksum (initial value)
            0               # Urgent pointer
        ) + self.data

        pseudo_hdr = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_ip),    # Source Address
            socket.inet_aton(self.dst_ip),    # Destination Address
            socket.IPPROTO_TCP,               # Protocol
            len(packet)                       # TCP Length
        )

        checksum = chksum(pseudo_hdr + packet)

        packet = packet[:16] + struct.pack('H', checksum) + packet[18:]

        return packet


class IPPacket:
    def __init__(self, src_ip, src_port, dst_ip, dst_port, data):
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.data = data

    def build(self):
        header = struct.pack(
            '!BBHHHBBH4s4s',
            69,                 # Version and IHL (=0x45)
            0,                  # Type of Service
            20,                 # Total Length
            0,                  # IP-ID
            0,                  # Fragment Offset
            64,                 # TTL
            socket.IPPROTO_TCP, # Protocol
            0,                  # Initial checksum
            self.src_ip,        # Source address
            self.dst_ip         # Destination address
        )

        checksum = chksum(header)

        header = header[:10] + struct.pack('H', checksum) + header[12:]

        return header + self.data

def tcp_send_and_receive(sock, src_ip, src_port, dst_ip, dst_port, data, tcp_seq):
    syn_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, 0, TCP_FLAGS_SYN, tcp_seq).build()
    syn_packet_ip = IPPacket(src_ip, src_port, dst_ip, dst_port, syn_packet_tcp).build()
    sock.sendto(syn_packet_ip, (dst_ip, dst_port))

    # TODO receive SYN-ACK
    syn_ack_packet = sock.recvfrom(2000)[0]
    # TODO send ACK
    # TODO send/receive packets
    # TODO only listen on src_port
    # TODO send FIN


parser = argparse.ArgumentParser ( description ='Super awesome TCP Client')
parser.add_argument ('src_ip', type=str)
parser.add_argument ('src_port', type=int)
parser.add_argument ('dst_ip', type=str)
parser.add_argument ('dst_port', type=int)
args = parser.parse_args ()

tcp_seq = random.randint (1, 60000)
sock = socket.socket ( socket.AF_INET , socket.SOCK_RAW , socket.IPPROTO_TCP )
sock.setsockopt ( socket.IPPROTO_IP , socket.IP_HDRINCL , 1)
sock.bind (( args.src_ip , args.src_port ))

# TODO set data
tcp_send_and_receive(sock, args.src_ip, args.src_port, args.dst_ip, args.dst_port, 0, tcp_seq)

# now you can send packets by sock.sendto ( packet_data , ( args.dst_ip , args.dst_port ))
# receiving packets is simple as sock.recvfrom (2000)

# packing packets is possible via struct.pack(format string, contents)