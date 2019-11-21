#!/usr/bin/env python3
from ping3 import ping
from joblib import Parallel, delayed
from socket import gethostbyaddr as lookup
from contextlib import closing
import time
import  socket
from prettytable import PrettyTable
import argparse

available = {}
startTime = time.time()

def dnsCheck(addr):
    try:
        name = lookup(addr)[0]
        return name
    except:
        return 'Not in DNS'

def pingTest(addr):

    try:
        if not ping(addr, timeout=1):
            available[addr] = dnsCheck(addr)
            return 'OK'
    except:
            return 'FAIL'

def pingCheck(subnet, netmask):

    if netmask == 24:
        Parallel(n_jobs=50, prefer="threads")(delayed(pingTest)(f"{subnet}.{i}") for i in range(10, 255))
    elif netmask == 23:
        octs = subnet.split('.')
        sub1 = subnet
        sub2 =f'{octs[0]}.{octs[1]}.{str(int(octs[2]) + 1)}'
        subs = [sub1, sub2]
        for sub in subs:
            Parallel(n_jobs=25, prefer="threads")(delayed(pingTest)(f"{sub}.{i}") for i in range(10, 255))
    elif netmask == 22:
        octs = subnet.split('.')
        sub1 = subnet
        sub2 =f'{octs[0]}.{octs[1]}.{str(int(octs[2]) + 1)}'
        sub2 =f'{octs[0]}.{octs[1]}.{str(int(octs[2]) + 2)}'
        subs = [sub1, sub2, sub3]
        for sub in subs:
            for i in range(10, 255):
                Parallel(n_jobs=16, prefer="threads")(delayed(pingTest)(f"{sub}.{i}") for i in range(10, 255))

def checkPort(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    socket.timeout(2)

    result = sock.connect_ex((addr, port))
    if result == 0:
        del available[addr]
    sock.close()

def portsCheck():
    ports = [3389, 22, 80, 443]
    for port in ports:
        try:
            Parallel(n_jobs=50, prefer="threads", timeout=2)(delayed(checkPort)(k, port) for k in available.keys())
        except:
            return False

def outTable():
    x = PrettyTable(['AVAILABLE IPs', 'DNS RESOLUTION'])
    for k,v in available.items():
        x.add_row([k, v])

    x.sortby = 'AVAILABLE IPs'
    print(x)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('subnet', help="Prvide first 3 octets of subnet you want to scan e.g. 10.33.40")
    parser.add_argument('-n', '--netmask', help="Provide netmask value (excepted values - 24, 23, 22, defulats to 24 if not specyfied)", default=24, type=int)
    args = parser.parse_args()

    pingCheck(args.subnet, args.netmask)
    portsCheck()
    outTable()



if __name__ == '__main__':
    main()
    print(f'--- {round((time.time() - startTime), 2)} seconds ---')
