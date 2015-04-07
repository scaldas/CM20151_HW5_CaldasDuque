import numpy as np 
import matplotlib as mpl
import csv

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

#Calculamos los delta
#Cada delta se calcula como (maximo - minimo)/1000
#Guardamos los minimos pues solo 

#El enunciado dice que debe ser de 1000³ sin embargo eso es algo descabellado y python no se puede ejecutar tal función pues no hay
#tanta memoria. Por esta rázón intentamos con una tamaño menor que es 300, el cual funciona bien. 
size = 300
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
					x_center = delta_x*(float(new_i) + 1/2)
					y_center = delta_y*(float(new_j) + 1/2)
					z_center = delta_z*(float(new_k) + 1/2)

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
print(rho)
print("Listo")

#1b. 
#Se encuentra la transformada inversa de Fourier de phi_gorrito que sabemos que phi_gorrito = -rho_gorrito. 
#Para esto se asume que rho_gorrito = rho
print('Se comienza a construir la matriz phi. Favor esperar y no entrar en pánico')
rho_gorrito= np.fft.fftn(rho)
phi_gorrito = rho_gorrito*(-1)
phi = np.fft.ifftn(phi_gorrito)
print('Listo')


#1c.
print('Finalmente se crea la matriz con las fuerzas')
#La fuerza la calculamos como F= -Grad(U) 
force = np.gradient(phi)*(-1)
print('Listo calisto!!')
# print(force)

minimos=[]
while len(minimos) < 150:
	for i in range(size):
		for j in range(size):
			for k in range(size):
				force[i,j,k]==min(force):
				minimos.append(force[i,j,k])
				data=np.delete(force, force[i,j,k])
print(type(force))		
# 
#maximos=[]
# while len(maximos) < 11:
# # 	if data[i]==max(data):
# # 		maximos.append(data[i])
# # 		data=np.delete(data, data[i])

# print(len(minimos))	

# mpl.plot()



