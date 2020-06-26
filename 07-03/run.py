import argparse
import random
import socket, struct
import array, time
import json
import hashlib

MAT_NR = 801005

# TCP flag constants
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
    def __init__(self, src_ip, src_port, dst_ip, dst_port, data, flags, seqnum = 0, acknum = 0, raw = False, dofs = 0):
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.data = data if raw else str.encode(data, 'utf-8')
        self.flags = flags
        self.seqnum = seqnum
        self.acknum = acknum
        self.dofs = dofs # for reserved flags

    def build(self):
        packet = struct.pack(
            '!HHLLBBHHH',
            self.src_port,        # Source Port
            self.dst_port,        # Destination Port
            self.seqnum,          # Sequence Number
            self.acknum,          # Acknowledgement Number
            (5 << 4) + self.dofs, # Data Offset
            self.flags,           # Flags
            8192,                 # Window
            0,                    # Checksum (initial value)
            0                     # Urgent pointer
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
    def __init__(self, src_ip, dst_ip, data, ip_id = 1):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.data = data
        self.ip_id = ip_id

    def build(self):
        header = struct.pack(
            '!BBHHHBBH4s4s',
            69,                                   # Version and IHL (=0x45)
            0,                                    # Type of Service
            20,                                   # Total Length
            self.ip_id,                           # IP-ID
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

def save_flags(syn_ack_flag, matriculation_flag, fin_flag):
    code_dict = {
        "matriculation_number" : matriculation_flag,
        "fin" : fin_flag,
        "synack": syn_ack_flag,
        "hours" : 8
    }
    fp = open('codes.json', 'w')
    fp.write(json.dumps(code_dict))
    fp.close()

def receive_and_acknowledge(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum, is_handshake = False, is_fin = False):
    while True:
        data_packet = sock.recvfrom(2000)[0]
        pack_dst = int.from_bytes(data_packet[22:24], byteorder='big')
        pack_src = int.from_bytes(data_packet[20:22], byteorder='big')
        if pack_dst != src_port or pack_src != dst_port:
            continue
        acknum = int.from_bytes(data_packet[28:32], byteorder='big')
        if is_handshake:
            seqnum = int.from_bytes(data_packet[24:28], byteorder='big') + 1
        else:
            seqnum += len(data_packet[40:])
        ip_id = int.from_bytes(data_packet[4:6], byteorder='big')
        send_flags = TCP_FLAGS_ACK
        if is_fin:
            send_flags += TCP_FLAGS_FIN
        ack_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, '', send_flags, acknum, seqnum).build()
        ack_packet_ip = IPPacket(src_ip, dst_ip, ack_packet_tcp).build()
        sock.sendto(ack_packet_ip, (dst_ip, dst_port))
        break
    return (ip_id, seqnum, acknum, data_packet)

def receive_instructions(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum, maxnum = 0):
    ip_id = 0
    counter = 0
    while ip_id != 0xffff:
        if maxnum > 0 and counter >= maxnum:
            break
        ip_id, seqnum, acknum, data = receive_and_acknowledge(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum)
        print(data[40:].decode())
        counter += 1
    return (ip_id, seqnum, acknum, data)

def left_packet(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum):
    matr_mod = MAT_NR % 2**16
    mat_nr_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, '', TCP_FLAGS_PSH + TCP_FLAGS_ACK, seqnum, acknum).build()
    mat_nr_packet_ip = IPPacket(src_ip, dst_ip, mat_nr_packet_tcp, ip_id=matr_mod).build()
    sock.sendto(mat_nr_packet_ip, (dst_ip, dst_port))
    return seqnum

def right_packet(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum):
    rsv_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, '', TCP_FLAGS_PSH + TCP_FLAGS_ACK, seqnum, acknum, dofs=14).build()
    rsv_packet_ip = IPPacket(src_ip, dst_ip, rsv_packet_tcp).build()
    sock.sendto(rsv_packet_ip, (dst_ip, dst_port))
    return seqnum

def top_packet(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum):
    payload = (0b111).to_bytes(1, byteorder='big')
    packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, payload, TCP_FLAGS_PSH + TCP_FLAGS_ACK, seqnum, acknum, raw=True).build()
    packet_ip = IPPacket(src_ip, dst_ip, packet_tcp).build()
    sock.sendto(packet_ip, (dst_ip, dst_port))
    return seqnum + 1

def bottom_packet(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum):
    payload = hashlib.md5(str(MAT_NR).encode('utf-8')).digest()
    packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, payload, TCP_FLAGS_PSH + TCP_FLAGS_ACK, seqnum, acknum, raw=True).build()
    packet_ip = IPPacket(src_ip, dst_ip, packet_tcp).build()
    sock.sendto(packet_ip, (dst_ip, dst_port))
    return seqnum + 16

def tcp_send_and_receive(sock, src_ip, src_port, dst_ip, dst_port, tcp_seq):
    syn_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, '', TCP_FLAGS_SYN, tcp_seq).build()
    syn_packet_ip = IPPacket(src_ip, dst_ip, syn_packet_tcp).build()
    sock.sendto(syn_packet_ip, (dst_ip, dst_port))

    syn_ack_flag, seqnum, acknum, data_packet = receive_and_acknowledge(sock, src_ip, src_port, dst_ip, dst_port, 0, 0, is_handshake = True)

    ip_id, seqnum, acknum, data_packet = receive_instructions(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum)

    mat_nr_packet_tcp = TCPPacket(src_ip, src_port, dst_ip, dst_port, str(MAT_NR) + '\r\n', TCP_FLAGS_PSH + TCP_FLAGS_ACK, acknum, seqnum).build()
    mat_nr_packet_ip = IPPacket(src_ip, dst_ip, mat_nr_packet_tcp).build()
    sock.sendto(mat_nr_packet_ip, (dst_ip, dst_port))
    
    ip_id, seqnum, acknum, data_packet = receive_instructions(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum, 2)
    ip_id, seqnum, acknum, data_packet = receive_and_acknowledge(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum, is_handshake = False)
    matriculation_flag = data_packet[40:].hex()

    ip_id, seqnum, acknum, data_packet = receive_instructions(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum)

    seqnum_before = seqnum
    seqnum, acknum = acknum, seqnum

    for _ in range(2):
        seqnum = bottom_packet(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum)
        time.sleep(0.1)
        
    for _ in range(4):
        seqnum = right_packet(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum)
        time.sleep(0.1)

    for _ in range(7):
        seqnum = top_packet(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum)
        time.sleep(0.1)
    
    for _ in range(4):
        seqnum = left_packet(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum)
        time.sleep(0.1)

    ip_id, seqnum, acknum, data_packet = receive_instructions(sock, src_ip, src_port, dst_ip, dst_port, seqnum_before, acknum)

    ip_id, seqnum, acknum, data_packet = receive_and_acknowledge(sock, src_ip, src_port, dst_ip, dst_port, seqnum, acknum, is_handshake = True, is_fin = True)

    while True:
        fin_packet = sock.recvfrom(2000)[0]
        pack_dst = int.from_bytes(fin_packet[22:24], byteorder='big')
        pack_src = int.from_bytes(fin_packet[20:22], byteorder='big')
        if pack_dst == src_port and pack_src == dst_port:
            break
    
    fin_data = fin_packet[40:].decode()
    print(fin_data)
    fin_flag = fin_data[29:]
    save_flags(syn_ack_flag, matriculation_flag, fin_flag)


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
