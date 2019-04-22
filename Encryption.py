import time, random, os
from time import sleep
import string

def power(x,n):
	if n == 1:
		return x
	if n%2 == 0:
		return power(x**2, int(n/2))
	if n%2 != 0:
		return x*power(x**2, int((n-1)/2))

def makePrimes():
	primes = []
	for i in range(100 ,1000):
		if checkPrime(i):
			primes.append(i)
	print("Primes generated")
	return primes

def checkPrime(n):
	for i in range(2,int(n**0.5)+1):
		if n%i == 0:
			return False
	return True

def privateKey(e):
	d = 1
	while (d<phi):
		if (d*e)%(phi) == 1:
			return d
		else:
			d += 1
			end = time.time()
			tt = end - st
			if tt > 10:
				print('Private key timeout')
				exit()

	return -1

os.system('clear')
primes = makePrimes()
p,q = primes[int(random.random()*(len(primes)-1))],primes[int(random.random()*(len(primes)-1))]
n = p*q
phi = (p-1)*(q-1)
p = 0

print('Public key created, key = %d, %d(n,phi)' %(n, phi))

st = time.time()

while(1):
	e = primes[p]
	d = privateKey(e)
	if d == -1:
		p += 1
	else:
		break

print('Private key created with e = %d -> %d'%(e,d))
m = input('message to send using RSA : ').encode('ascii')
print('Sending in packets....')
#sleep(2)
total_message = ''
for byte in m:
	c = power(byte,e)%n
	print('Sending encrypted message : %d'%c)
	decrypted = chr(power(c,d)%n)
	total_message += decrypted
	print('decrypted message -> %s'%decrypted)
print('Total message received = %s'%total_message)

'''
if m<n:
	c = (m**e)%n
	print('Sending encrypted message : %d'%c)
	sleep(1)
	decrypted = (c**d)%n
	print('decrypted message -> %d'%chr(decrypted))

else:
	m = str(m)
	total_message = ''
	print('Sending in packets....')
	sleep(2)
	stride = len(str(n))-1
	for i in range(0,len(m),stride):
		digit = int(m[i:i+stride])
		c = (digit**e)%n
		print('Sending encrypted message : %d'%c)
		sleep(1)
		decrypted = (c**d)%n
		total_message += str(decrypted)
		print('decrypted message -> %d'%decrypted)
	print('Total message received = %s'%total_message)
'''