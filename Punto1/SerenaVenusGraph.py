import numpy as np 
import matplotlib as mpl
import csv


with open('Serena-Venus.txt','r') as f:
	raw_data = f.readlines()

x_coord=[]
y_coord=[]
z_coord=[]

for line in raw_data:
	particle = line.split( )
	x_coord.append(float(particle[1]))
	y_coord.append(float(particle[2]))
	z_coord.append(float(particle[3]))


with open('force.csv','r') as f1:
	raw_data1 = f1.readlines()

data=[]
for line in raw_data1:
	data.append(line)
phi= np.array(data)

minimos=[]
while len(minimos) < 11:
	if data[i]==min(data):
		minimos.append(data[i])
		data=np.delete(data, data[i])
		
maximos=[]
while len(maximos) < 11:
	if data[i]==max(data):
		maximos.append(data[i])
		data=np.delete(data, data[i])

print(len(maximos))	

mpl.plot()



