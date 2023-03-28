from scapy.all import sr1, srp, send, wrpcap, IP, ICMP
from random import randint

DST_URL = "www.instagram.com"

SRC_PORT = randint(1024, 65535)
HTTPS_PORT = 443


def getPing():
    packet = IP(dst=DST_URL) / ICMP()
    response = sr1(packet, timeout=1)
    return [packet, response]


wrpcap("PING_request_response_2001CS19.pcap", getPing())