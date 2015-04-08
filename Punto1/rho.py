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

#LA VARIABLE SIZE DEFINE EL TAMANIO DE LA MATRIZ Y PUEDE VARIARSE. POR FAVOR LEER LAS ANOTACIONES.
size = 100

#Calculamos los delta
#Cada delta se calcula como (maximo - minimo)/size
#Guardamos los minimos pues seran de utilidad mas adelante
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

#Inicializamos la matriz
rho = np.zeros((size, size, size))
num_puntos = np.zeros((size, size, size))

#Construimos rho
for i in range(0,len(x_coord)):
	x = x_coord[i]
	y = y_coord[i]
	z = z_coord[i]

	i = int((x-min_x)/delta_x)
	j = int((y-min_y)/delta_y)
	k = int((z-min_z)/delta_z)

	#Las particulas que caigan en los limites superiores de la grilla se cuentan en la ultima celda
	if i == size:
		i = size - 1
	if j == size:
		j = size - 1
	if k == size:
		k = size - 1


	#El peso estadistico de cada particula depende de su masa. Como todas las masas son 1, m = 1
	m = 1.0

	#Agregamos la particula no solo a la celda en la que se encuentra sino a las adyacentes donde pudiera ser relevante
	#El algortimo se hace asi para hacerlo mas eficiente
	#No es posible que una particula afecte una celda que no sea su vecina. Sin embargo, se deben revisar los vecinos en las tres dimensiones
	for a in range(-1,1):
		for b in range(-1,1):
			for c in range(-1,1):
				new_i = i + a
				new_j = j + b
				new_k = k + c
				
				#Los limites de la grilla tendran algunos vecinos que esten fuera de la grilla
				if new_i < size and new_j < size and new_k < size and new_i > -1 and new_j > -1 and new_k > -1:
					x_center = min_x + delta_x*(float(new_i) + 0.5)
					y_center = min_y + delta_y*(float(new_j) + 0.5)
					z_center = min_z + delta_z*(float(new_k) + 0.5)

					if abs(x-x_center) < delta_x:
						W_x = 1.0 - (abs(x-x_center)/delta_x)
					else:
						W_x = 0.0

					if abs(y-y_center) < delta_y:
						W_y = 1.0 - (abs(y-y_center)/delta_y)
					else:
						W_y = 0.0
					
					if abs(z-z_center) < delta_z:
						W_z = 1.0 - (abs(z-z_center)/delta_z)
					else:
						W_z = 0.0

					rho[new_i,new_j,new_k] += W_x*W_y*W_z

rho = (m/(delta_x*delta_y*delta_z))*rho

print("Se ha creado rho. Inicia Impresion...")

#Imprimimos rho para revisar que no quede en ceros
#print(rho)

#Se imprimen los resultados obtenidos en un archivo
#Se sigue el formato del programa XPRESS (optimizador lineal)
with open('rho.txt','w') as f:
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
				f.write("(%d,%d,%d)%f\n" % (i,j,k,rho[i,j,k]))

print("Finaliza Impresion.")