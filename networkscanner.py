import subprocess
import ipaddress
import sys

def ipSubnet(ipsub):
    net = ipaddress.ip_network(ipsub)
    hosts = []
    for x in net:
        hosts.append(str(x))
    return hosts

def ping(host):
    args = ["ping", "-w", "1", host]
    p = subprocess.Popen(args, bufsize=100000, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[0]
    output = bytes.decode(output)
    if "rtt" in output:
        print(host + " is alive")
        return host
    return None

def scan(host, mode):
    ports = []
    if mode == "tcp":
        print("Start TCP scan on " + host)
        args = "nc -z -v -w 1 " + host
    elif mode == "udp":
        print("Start UDP scan on " + host)
        args = "nc -z -v -u " + host
    for i in range(1, 101):
        process = subprocess.Popen(
            args + " " + str(i), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = bytes.decode(process.stderr.read())
        print(output)
        if "succeeded" in output:
            data = output.strip().split(' ')
            ports.append(data[3]+ " " + data[5])
    return {host: ports}

if __name__ == '__main__':
    if '/' in sys.argv[1]:
        ipsub = sys.argv[1]
        hosts = ipSubnet(ipsub)
        listHosts = []
        for host in hosts:
            if ping(host) is not None:
                r1 = scan(host, "tcp")
                #r2 = scan(host, "udp")
                for x, y in r1.items():
                    for k in y:
                        print(x + " " + k + '\n')
        if len(listHosts) == 0:
            print("No host")
    else:
        host = sys.argv[1]
        if ping(host) is not None:
                r1 = scan(host, "tcp")
                #r2 = scan(host, "udp")
                for x, y in r1.items():
                    for k in y:
                        print(x + " " + k + '\n')
        else:
            print(host + " is down")
            print("Exit")
