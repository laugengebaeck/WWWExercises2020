import argparse
import random
import socket, struct
import array
import codecs

# TCP flag constants
TCP_FLAGS_RSV = (1 << 9)
TCP_FLAGS_NOC = (1 << 8)
TCP_FLAGS_CWR = (1 << 7)
TCP_FLAGS_ECN = (1 << 6)
TCP_FLAGS_URG = (1 << 5)
TCP_FLAGS_ACK = (1 << 4)
TCP_FLAGS_PSH = (1 << 3)
TCP_FLAGS_RST = (1 << 2)
TCP_FLAGS_SYN = (1 << 1)
TCP_FLAGS_FIN = (1)

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
        self.data = str.encode(data, 'utf-8')
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
    def __init__(self, src_ip, dst_ip, data):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.data = data

    def build(self):
        header = struct.pack(
            '!BBHHHBBH4s4s',
            69,                                   # Version and IHL (=0x45)
            0,                                    # Type of Service
            20,                                   # Total Length
            1,                                    # IP-ID
            0,                                    # Fragment Offset
            64,                                   # TTL
            socket.IPPROTO_TCP,                   # Protocol
            0,                                    # Initial checksum
            socket.inet_aton(self.src_ip),        # Source address
            socket.inet_aton(self.dst_ip)         # Destination address
        )

        checksum = chksum(header)

        header = header[:10] + struct.pack('H', checksum) + header[12:]

        return header + self.data

def tcp_send_and_receive(sock, src_ip, src_port, dst_ip, dst_port, tcp_seq):
    syn_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, '', TCP_FLAGS_SYN, tcp_seq).build()
    syn_packet_ip = IPPacket(src_ip, dst_ip, syn_packet_tcp).build()
    sock.sendto(syn_packet_ip, (dst_ip, dst_port))

    syn_ack_packet = sock.recvfrom(2000)[0]
    # sequence number is indices 24 to 28, ack number is indices 28 to 32 
    seqnum_str = ''.join('%02x' % ord(c) for c in syn_ack_packet[24:28].decode())
    seqnum = int(seqnum_str, base=16)
    acknum_str = ''.join('%02x' % ord(c) for c in syn_ack_packet[28:32].decode())
    acknum = int(acknum_str, base=16)

    ack_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, '', TCP_FLAGS_ACK, acknum, seqnum+1).build()
    ack_packet_ip = IPPacket(src_ip, dst_ip, ack_packet_tcp).build()
    sock.sendto(ack_packet_ip, (dst_ip, dst_port))

    # TODO interaction
    # IP-ID of first packet [4:6] is synack code
    # TCP_FLAG_PSH has to be set in matriculation number packet

    # TODO send FIN
    #sequence_number_fin = tcp_seq # TODO sequence number mitzählen
    #fin_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, '', TCP_FLAGS_FIN, sequence_number_fin).build()
    #fin_packet_ip = IPPacket(src_ip, dst_ip, fin_packet_tcp).build()
    #sock.sendto(fin_packet_ip, (dst_ip, dst_port))

    #TODO save flags


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

tcp_send_and_receive(sock, args.src_ip, args.src_port, args.dst_ip, args.dst_port, tcp_seq)

# now you can send packets by sock.sendto ( packet_data , ( args.dst_ip , args.dst_port ))
# receiving packets is simple as sock.recvfrom (2000)

# packing packets is possible via struct.pack(format string, contents)