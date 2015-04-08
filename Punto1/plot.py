import numpy as np 
import csv, os
import scipy.fftpack as fftp
import matplotlib.pyplot as plt


#Se reconstruye la informacion necesaria a partir del archivo forces.txt
with open('forces.txt','r') as f:
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


F = np.zeros((size-1,size-1,size-1))
for line in raw_data[7:]:
	i = line.index("(")
	f =	line.index(")")
	indexes = line[i+1:f].rsplit(",")
	value = line[f+1:]
	F[int(indexes[0]), int(indexes[1]), int(indexes[2])] = value

#Tambien es necesario las posiciones reales de los puntos
#Extraemos la informacion del archivo
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

#Ahora encontramos el minimo y maximo
minimo = F.min()
maximo = F.max()

#Ahora encontramos la posicion del maximo y minimo 
minindex = np.where(F==minimo)
p_x = (minindex[0] + 0.5)*delta_x + min_x
p_y = (minindex[1] + 0.5)*delta_y + min_y
p_z = (minindex[2] + 0.5)*delta_z + min_z
posicion_min= [p_x, p_y, p_z]

maxindex = np.where(F==maximo)
p1_x = (maxindex[0]+ 0.5)*delta_x + min_x
p1_y = (maxindex[1] + 0.5)*delta_y + min_y
p1_z = (maxindex[2] + 0.5)*delta_z + min_z
posicion_max= [p1_x, p1_y, p1_z]

print(minimo)
print(maximo)

#Ahora queremos graficar en un plano 
F_proyeccion = F[:,:,0]
for i in range(1, size-1):
    F_proyeccion = F_proyeccion + F[:,:,i]


fig, axs = plt.subplots(1,2)
plt.figure(figsize=(12,8))
fig.suptitle("Comparacion de contornos de la fuerza gravitacional\n y distribucion de particulas", fontsize=16)
fig.set_size_inches(18.5,8.5)
x = np.zeros(size-1)
y = np.zeros(size-1)
for i in range(0,size-1):
	x[i] = (2*i+1)*0.5*delta_x + min_x
	y[i] = (2*i+1)*0.5*delta_y + min_y
levels = np.linspace(F_proyeccion.min(), F_proyeccion.max(), 10)
cs = axs[0].contourf(x, y, F_proyeccion, levels=levels, label="Gravitational Force")
fig.colorbar(cs, ax=axs[0], format="%.0f")
cs= axs[0].contour(x, y, F_proyeccion, 8, colors='black', linewidth=.5)
cs = axs[1].plot(x_coord, y_coord,'mo', markersize = 1, label="Particles")
axs[1].set_axis_bgcolor('white')

fig.savefig('plot.png')
