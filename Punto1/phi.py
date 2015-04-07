import numpy as np 
import csv, os
import scipy.fftpack as fftp

#Se reconstruye la informacion necesaria a partir del archivo rho.txt
with open('rho.txt','r') as f:
	raw_data = f.readlines()

def getValue(line):
	return line[line.index(")")+1:]
line = raw_data[0]
size = int(getValue(line))
line = raw_data[1]
min_x = float(getValue(line))
line = raw_data[2]
min_y = float(getValue(line))
line = raw_data[3]
min_z = float(getValue(line))
line = raw_data[4]
delta_x = float(getValue(line))
line = raw_data[5]
delta_y = float(getValue(line))
line = raw_data[6]
delta_z = float(getValue(line))


rho = np.zeros((size,size,size))
for line in raw_data[7:]:
	i = line.index("(")
	f =	line.index(")")
	indexes = line[i+1:f].rsplit(",")
	value = line[f+1:]
	rho[int(indexes[0]), int(indexes[1]), int(indexes[2])] = value

#1b. 
#Se encuentra la transformada inversa de Fourier de phi_gorrito
#Sabemos que phi_gorrito = -rho_gorrito. 
print('Se comienza a construir la matriz phi. Favor esperar y no entrar en panico')
rho_gorrito= np.fft.fftn(rho)
phi_gorrito = rho_gorrito*(-1)
phi = np.fft.ifftn(phi_gorrito)
phi = abs(phi)
print('Listo. Comenzando Impresion...')

#Imprimimos phi para revisar que no haya complejos
#print(phi)

#Se imprimen los resultados obtenidos en un archivo
#Se sigue el formato del programa XPRESS (optimizador lineal)
with open('phi.txt','w') as f:
	f.write("(size)%d\n" % (size))
	f.write("(min_x)%f\n" % (min_x))
	f.write("(min_y)%f\n" % (min_y))
	f.write("(min_z)%f\n" % (min_z))
	f.write("(delta_x)%f\n" % (delta_x))
	f.write("(delta_y)%f\n" % (delta_y))
	f.write("(delta_z)%f\n" % (delta_z))
	for i in range(0,size):
		for j in range(0,size):
			for k in range(0,size):
				f.write("(%d,%d,%d)%f\n" % (i,j,k,phi[i,j,k]))

print("Finaliza Impresion.")