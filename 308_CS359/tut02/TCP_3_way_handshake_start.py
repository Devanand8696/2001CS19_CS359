from scapy.all import sr1, srp, send, wrpcap, IP, TCP
from random import randint

DST_URL = "www.instagram.com"

SRC_PORT = randint(1024, 65535)
HTTPS_PORT = 443


def getTCPHandshakeStart():
    ip = IP(dst=DST_URL)

    syn = ip / TCP(sport=SRC_PORT, dport=HTTPS_PORT, flags="S", seq=0)
    syn_ack = sr1(syn)
    ack = ip / TCP(
        sport=SRC_PORT,
        dport=HTTPS_PORT,
        flags="A",
        seq=syn_ack.ack,
        ack=syn_ack.seq + 1,
    )

    return [syn, syn_ack, ack]


wrpcap("TCP_3_way_handshake_start_2001CS19.pcap", getTCPHandshakeStart())
