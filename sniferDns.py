from os import system
from scapy.all import sniff
from scapy.all import ARP
from scapy.all import DNSQR
from scapy.all import UDP
from scapy.all import IP
from scapy.all import IPv6
from scapy.all import DNS
import ipaddress
import logging
import logging.handlers
from ipreputation import abuseipdb
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)


def process(pkt):
    ip46 = IPv6 if IPv6 in pkt else IP
    #note chnage it to what you need it -> "pkt[UDP].*sport* == 53"
    if pkt.haslayer(DNSQR) and UDP in pkt and pkt[UDP].sport == 53 and ip46 in pkt:
        query = pkt[DNS].qd.qname.decode("utf-8") if pkt[DNS].qd != None else "?"
        if pkt[DNS].qd.qtype == 1:
            try:
                ipaddress.ip_address(str(pkt[DNS].an.rdata))
                ip_s = abuseipdb(pkt[DNS].an.rdata)
                print(pkt[ip46].src, pkt[ip46].dst, query, pkt[DNS].an.rdata)
                my_logger.info('{},{},{},{},{}'.format(pkt[ip46].src, pkt[ip46].dst, query, pkt[DNS].an.rdata,ip_s.Abusescore()))
            except Exception as e:
                pass
        else:
            print(pkt[ip46].src, pkt[ip46].dst, query,'NOT TYPE A')



if __name__ == "__main__":
    #name of the interface
    iface = ''
    sniff(filter='udp port 53', store=0, prn=process, iface=iface)
