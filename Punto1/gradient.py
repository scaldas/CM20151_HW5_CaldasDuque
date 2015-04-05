import numpy as np
import csv


with open('phi.csv','r') as f:
	raw_data = f.readlines()

#Se crea un arreglo y se llena con los datos de phi
data=[]
for line in raw_data:
	data.append(line)
phi= np.array(data)

#La fuerza la calculamos como F= -Grad(U) 
force = np.gradient(phi, dtype=np.float))*(-1)

np.savetxt('force.csv', force, delimiter=',')
