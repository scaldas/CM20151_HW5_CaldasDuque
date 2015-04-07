import numpy as np 
import csv, os
import scipy.fftpack as fftp


#Extraemos la informacion del archivo
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
size = 100
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

print("Inicializa la matriz")
#Construimos rho
rho = np.zeros((size, size, size))
num_puntos = np.zeros((size, size, size))

print("Comienza a construir rho")
for i in range(0,len(x_coord)):
	x = x_coord[i]
	y = y_coord[i]
	z = z_coord[i]

	i = int((x-min_x)/delta_x)
	j = int((y-min_y)/delta_y)
	k = int((z-min_z)/delta_z)

	if i == size:
		i = size - 1
	if j == size:
		j = size - 1
	if k == size:
		k = size - 1

	#DUDA!
	#Sigo sin saber cual masa utilizar
	#Uso solo la de la celda o la que esta fuera tambien?
	num_puntos[i,j,k] += 1

	for a in range(-1,1):
		for b in range(-1,1):
			for c in range(-1,1):

				new_i = i + a
				new_j = j + b
				new_k = k + c
				
				if new_i < size and new_j < size and new_k < size and new_i > -1 and new_j > -1 and new_k > -1:
					x_center = min_x + delta_x*(float(new_i) + 0.5)
					y_center = min_y + delta_y*(float(new_j) + 0.5)
					z_center = min_z + delta_z*(float(new_k) + 0.5)

					if abs(x-x_center) < delta_x:
						W_x = 1 - (abs(x-x_center)/delta_x)
					else:
						W_x = 0

					if abs(y-y_center) < delta_y:
						W_y = 1 - (abs(y-y_center)/delta_y)
					else:
						W_y = 0
					
					if abs(z-z_center) < delta_z:
						W_z = 1 - (abs(z-z_center)/delta_z)
					else:
						W_z = 0

					rho[new_i,new_j,new_k] += W_x*W_y*W_z

					#Descomentar esta linea si cada nube cuenta en cada celda
					#if W_x != 0 and W_y != 0 and W_z != 0:
					#	num_puntos[new_i,new_j,new_k] += 1

rho = num_puntos*rho
rho = (1/(delta_x*delta_y*delta_z))*rho

print("Listo")
#Imprimimos rho para revisar que no quede en ceros
#print(rho)

#1b. 
#Se encuentra la transformada inversa de Fourier de phi_gorrito que sabemos que phi_gorrito = -rho_gorrito. 
#Para esto se asume que rho_gorrito = rho
print('Se comienza a construir la matriz phi. Favor esperar y no entrar en panico')
phi_gorrito= rho*(-1)
phi = np.fft.ifftn(phi_gorrito)
phi = abs(phi)
print('Listo')
#Imprimimos phi para revisar que no haya complejos
#print(phi)

#1c.
print('Finalmente se crea la matriz con las fuerzas')
#La fuerza la calculamos como F = -Grad(U) 

force = np.gradient(phi)
force = np.asarray(force)
force = (-1)*force

#Imprimimos la fuerza para cersiorarnos que el arreglo no este vacio
#print(force)
print('Listo calisto!!')
