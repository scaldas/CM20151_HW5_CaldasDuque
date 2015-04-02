import numpy as np
import csv, os
import time

#Leemos la informacion del archivo
with open('Serena-Venus.txt','r') as f:
	raw_data = f.readlines()

#Guardamos las coordenadas x,y,z de cada particula
x_coord=[]
y_coord=[]
z_coord=[]

for line in raw_data:
	particle = line.split( )
	x_coord.append(float(particle[1]))
	y_coord.append(float(particle[2]))
	z_coord.append(float(particle[3]))

#Probamos imprimiendo la informacion de las 5 primeras particulas
#for i in range(0,5):
#	print("%f, %f, %f" % (x_coord[i], y_coord[i], z_coord[i]))

#Calculamos los delta
#Cada delta se calcula como (maximo - minimo)/1000
#Guardamos los minimos pues solo 
size = 1000
min_x = min(x_coord)
min_y = min(y_coord)
min_z = min(z_coord)

delta_x = (max(x_coord) - min_x)/size
delta_y = (max(y_coord) - min_y)/size
delta_z = (max(z_coord) - min_z)/size

#Imprimimos los delta
#print("dx = %f" % (delta_x))
#print("dy = %f" % (delta_y))
#print("dz = %f" % (delta_z))

#Construimos rho_gorrito
rho_gorrito = np.zeros((size, size, size))
num_puntos = np.zeros((size, size, size))

for i in range(0,len(x_coord)):
	x = x_coord[i]
	y = y_coord[i]
	z = z_coord[i]

	i = int((x-min_x)/delta_x)
	j = int((y-min_y)/delta_y)
	k = int((z-min_z)/delta_z)

	if(i == 1000):
		i = 999
	if(j == 1000):
		j = 999
	if(k == 1000):
		k = 999

	x_center = i + delta_x/2
	y_center = j + delta_y/2
	z_center = k + delta_z/2

	W_x = 1 - (abs(x-x_center)/delta_x)
	W_y = 1 - (abs(y-y_center)/delta_y)
	W_z = 1 - (abs(z-z_center)/delta_z)

	num_puntos[i,j,k] += 1
	rho_gorrito[i,j,k] += W_x*W_y*W_z

rho_gorrito = num_puntos*rho_gorrito
rho_gorrito = (1/(delta_x*delta_y*delta_z))*rho_gorrito






