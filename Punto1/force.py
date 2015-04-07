import numpy as np 
import csv, os
import scipy.fftpack as fftp

#Se reconstruye la informacion necesaria a partir del archivo phi.txt
with open('phi.txt','r') as f:
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


phi = np.zeros((size,size,size))
for line in raw_data[7:]:
	i = line.index("(")
	f =	line.index(")")
	indexes = line[i+1:f].rsplit(",")
	value = line[f+1:]
	phi[int(indexes[0]), int(indexes[1]), int(indexes[2])] = value

#1c.
print('Se crea la matriz con las fuerzas')

#La fuerza la calculamos a partir de sus componentes como sqrt(F_x^2+F_y^2+F_z^2)
#Por ejemplo, la componente en x se calcula como F_x = - dphi/dx
#Por la naturaleza del metodo usado, se pierde la informacion del limite superior de cada dimension
F_x = (phi[1:,:,:] - phi[:-1,:,:])[:,:-1,:-1]/delta_x
F_y = (phi[:,1:,:] - phi[:,:-1,:])[:-1,:,:-1]/delta_y
F_z = (phi[:,:,1:] - phi[:,:,:-1])[:-1,:-1,:]/delta_z

F_x = -1*F_x
F_y = -1*F_y
F_z = -1*F_z

F = ((F_x**2)+(F_y**2)+(F_z**2))**(0.5)

print('Listo. Comenzando Impresion...')

#Imprimimos la fuerza para cersiorarnos que el arreglo no este vacio ni lleno de unos
#print(F)

#Se imprimen los resultados obtenidos en un archivo
#Se sigue el formato del programa XPRESS (optimizador lineal)
with open('forces.txt','w') as f:
	f.write("(size)%d\n" % (size))
	f.write("(min_x)%f\n" % (min_x))
	f.write("(min_y)%f\n" % (min_y))
	f.write("(min_z)%f\n" % (min_z))
	f.write("(delta_x)%f\n" % (delta_x))
	f.write("(delta_y)%f\n" % (delta_y))
	f.write("(delta_z)%f\n" % (delta_z))
	for i in range(0,size-1):
		for j in range(0,size-1):
			for k in range(0,size-1):
				f.write("(%d,%d,%d)%f\n" % (i,j,k,F[i,j,k]))

print("Finaliza Impresion.")