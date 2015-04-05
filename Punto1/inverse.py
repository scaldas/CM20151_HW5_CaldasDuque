import numpy as np 
import csv, os
import scipy.fftpack as fftp


#Se lee el archivo de texto creado en el punto anterior
with open('rho_gorrito.csv','r') as f:
	raw_data = f.readlines()

#Se crea un arreglo y se llena con los datos de rho_gorrito
data=[]
for line in raw_data:
	data.append(line)
rho_gorrito= np.array(data)

#
phi_gorrito= rho_gorrito*(-1)
phi = np.fft.ifftn(phi_gorrito)

np.savetxt('phi.csv', phi, delimiter=',')

