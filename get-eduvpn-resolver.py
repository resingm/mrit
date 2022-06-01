#!/usr/bin/env python3

########################################################################
# 
# get-eduvpn-resolver.py
#
# Miniscript that returns the resolver as defined for each of the EduVPN
# secure internet access VPN servers. Required for some research. Tool
# might not be useful for anyone else.
#
########################################################################


import sys

DNS_RESOLVER = {
    "eduvpn1.eduvpn.de" : "192.129.31.50,192.129.31.54,192.129.31.58,2001:638:d:b201::1",
    "eduvpn1.funet.fi": "193.166.4.24,193.166.4.25",
    "eduvpn.ac.lk" : "192.248.1.161",
    "eduvpn.cynet.ac.cy" : "82.116.200.250,82.116.200.245",
    "eduvpn.deic.dk": "130.226.1.2",
    "eduvpn.eenet.ee": "193.40.0.12",
    "eduvpn.kenet.or.ke": "9.9.9.9,2620:fe::fe",
    "eduvpn.myren.net.my": "203.80.16.81,203.80.21.205,2404:a8:10::81,2001:4860:4860::8888",
    "eduvpn-poc.renater.fr": "193.49.159.2,193.49.159.9",
    "eduvpn.rash.al": "1.1.1.1,8.8.8.8",
    "eduvpn.renu.ac.ug": "196.43.185.3,196.43.185.35",
    "eduvpn.uran.ua": "212.111.192.35,2a01:5c40::2:2",
    "guest.eduvpn.ac.za": "9.9.9.9,149.112.112.112",
    "guest.eduvpn.no": "2001:700:0:ff00::1,158.38.0.1",
    "nl.eduvpn.org": "192.87.36.36,192.87.106.106,2001:610:3:200a:192:87:36:36,2001:610:1:800a:192:87:106:106",
    "vpn.pern.edu.pk": "8.8.8.8",
}

def main():
    vpn = next(sys.stdin)
    vpn = vpn.strip(" \t\r\n")
    resolver = ""

    if vpn in DNS_RESOLVER.keys():
        _resolver = DNS_RESOLVER[vpn]
        _resolver = _resolver.split(",")

        if len(_resolver):
            resolver = _resolver[0]

    sys.stdout.write(f"{resolver}\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()