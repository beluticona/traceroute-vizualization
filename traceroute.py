#!/usr/bin/python

# This programs allow you to analyze the IP route and the distance of each step by sendind IP packets to a given direction. You can specify the numbers os step to be count, if not provided it uses a default value.
 
# Run sudo python traceroute.py [dirIP] [#packets] [#steps]

import sys
from scapy.all import *
from scapy.layers.inet import IP, ICMP, sr1
from time import *
import statistics
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geocoder


#default
responses = {}
cant_paquetes = 1
cant_saltos = 18
rtts = []
file_name_dist = 'distances.csv'
file_name_ips = 'IPs.csv'

#args
if len(sys.argv) >= 3:
	cant_paquetes = sys.argv[2]
	file_name_dist ='dist_p'+cant_paquetes
	file_name_ips = 'ips_p' +cant_paquetes
	cant_paquetes = int(cant_paquetes)
	if (len(sys.argv) >= 4):
		cant_saltos = sys.argv[3]
		file_name_dist = file_name_dist + '_s' + cant_saltos
		file_name_ips = file_name_ips + '_s' + cant_saltos
		cant_saltos = int(cant_saltos)
	file_name_dist+='.csv'
	file_name_ips+='.csv'
	
	
def medicion_de_mayor_repetido(dicIPWithTime):
	max_appear = 0
	nodo = None
	for ip in dicIPWithTime:
		if len(dicIPWithTime[ip]) > max_appear:
			max_appear = len(dicIPWithTime[ip])
			nodo = ip
	return (nodo, statistics.mean(dicIPWithTime[ip]))#,statistics.stdev(dicIPWithTime[ip]))

for ttl in range(1,cant_saltos):
	for i in range(cant_paquetes):
		probe = IP(dst=sys.argv[1], ttl=ttl) / ICMP()
		t_i = time()
		ans = sr1(probe, verbose=False, timeout=0.8)
		t_f = time()
		rtt = (t_f - t_i)*1000
		if ans is not None:
			if ttl not in responses: responses[ttl] = {}
			if ans.src not in responses[ttl]: responses[ttl][ans.src] = []
			responses[ttl][ans.src].append(rtt)
		#if ttl in responses: print (ttl, responses[ttl])

mediciones = []
for ttl in responses:
	mediciones.append(medicion_de_mayor_repetido(responses[ttl]))

rtt_por_salto = []
for i in range(len(mediciones)-2):
	rtt_por_salto.append([mediciones[i][0],mediciones[i+1][0],mediciones[i+1][1]-mediciones[i][1]])


file_dist = open(file_name_dist,'w')
file_dist.write('src,dst,rtt\n')
for rtt in rtt_por_salto:
	if rtt[2] >= 0:
		file_dist.write(rtt[0])
		file_dist.write(',')
		file_dist.write(rtt[1])
		file_dist.write(',')
		file_dist.write(str(rtt[2]))
		file_dist.write("\n")
file_dist.close()

i = 0

file_ips = open(file_name_ips,'w')
file_ips.write('i node,IP\n')
for ttl in responses:
	print('node:',i)
	for ip_i in responses[ttl]:
		file_ips.write(str(i))
		file_ips.write(',')
		file_ips.write(ip_i)
		file_ips.write('\n')
		print(ip_i)
	i = i+1		
file_ips.close()



#PLOTS


rtts = pd.read_csv(file_name_dist, header=0)

x=np.arange(0,len(rtts["rtt"]),1)
y = rtts["rtt"]

plt.plot(x,y)
plt.xlabel("i node")
plt.ylabel("Time per step")

_ips = pd.read_csv(file_name_ips, header=0)

destinos = _ips["IP"]

for i in range(0, len(destinos)):
    g = geocoder.ip(destinos[i])
    destinos[i] = g.city

file_ips = open('cities' + file_name_ips,'w')
file_ips.write('i node, city\n')
i=0
for ciudad in destinos:
	print('node:',ciudad)
	file_ips.write(str(i))
	file_ips.write(',')
	file_ips.write(str(ciudad))
	file_ips.write('\n')
	i = i+1		
file_ips.close()







