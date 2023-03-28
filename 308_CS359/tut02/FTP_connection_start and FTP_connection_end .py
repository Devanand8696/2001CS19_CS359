from scapy.all import *

def job(dstIP, roll):
    pkt = (IP(dst=dstIP) / TCP(sport=RandShort(),
                               dport=21,flags="S",options=[
                                   ('MSS', 1460), ('SAckOK', ''),
                                   ('Timestamp', (5693231, 0)),
                                   ('NOP', None), ('WScale', 6)
                                   ]
                               ))
    wrpcap(f"FTP_open_connection_2001CS{roll}.pcap",pkt)
    ans=sr1(pkt)
    wrpcap(f"FTP_open_connection_2001CS{roll}.pcap",ans,append=True)

    sseq=ans.seq
    sack=ans.ack

    ack=(IP(proto=6, tos=0, dst=dstIP, options='',
            version=4)/TCP(seq=sack, ack=sseq+1, dport=21, flags="A", options=[
                ('NOP', None),
                ('NOP', None),
                ('Timestamp', (981592, 525503134))
                ]))
    wrpcap(f"FTP_open_connection_2001CS{roll}.pcap",ack,append=True)
    ans=sr1(ack)

    # FINI START
    fin=(IP(proto=6, tos=0, dst=dstIP, options='',
            version=4)/TCP(dport=21, flags="F", options=[
                ('NOP', None),
                ('NOP', None),
                ('Timestamp', (981592, 525503134))
                ]))
    wrpcap(f"FTP_connection_end_2001CS{roll}.pcap",fin)
    ans=sr1(fin)
    wrpcap(f"FTP_connection_end_2001CS{roll}.pcap",ans, append=True)
    ack=(IP(proto=6, tos=0, dst=dstIP, options='',
            version=4)/TCP(dport=21, flags="A", options=[
                ('NOP', None),
                ('NOP', None),
                ('Timestamp', (981592, 525503134))
                ]))
    wrpcap(f"FTP_connection_end_2001CS{roll}.pcap",ack, append=True)


if _name_ == "_main_":
    conf = [['75.101.155.12', 19],
            ['204.236.238.164', 26],
            ['50.18.44.221', 16],
            ['52.32.19.90', 15]]
    for ip, r in conf:
        job(ip, r)
