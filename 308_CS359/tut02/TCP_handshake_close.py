from scapy.all import sr1, srp, send, wrpcap, IP, TCP
from random import randint

DST_URL = "www.instagram.com"

SRC_PORT = randint(1024, 65535)
HTTPS_PORT = 443


def getTCPHandshakeEnd():
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
    send(ack)
    fin = IP(dst=syn_ack.src) / TCP(
        sport=SRC_PORT,
        dport=HTTPS_PORT,
        flags="FA",
        seq=syn_ack.ack,
        ack=syn_ack.seq + 1,
    )
    fin_ack = sr1(fin, timeout=3)
    res = [syn, syn_ack, ack, fin, fin_ack]

    return res


wrpcap("TCP_handshake_close_2001CS19.pcap", getTCPHandshakeEnd())
