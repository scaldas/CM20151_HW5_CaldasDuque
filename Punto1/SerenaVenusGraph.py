import numpy as np 
import csv, os
import scipy.fftpack as fftp
import matplotlib.pyplot as plt


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
#Guardamos los minimos pues seran de utilidad mas adelante
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

print('Se comienza a construir la matriz rho')
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

	#DUDA!
	#Sigo sin saber cual masa utilizar
	#Uso solo la de la celda o la que esta fuera tambien?
	#num_puntos[i,j,k] += 1

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

					#Descomentar esta linea si cada nube cuenta en cada celda
					#if W_x != 0 and W_y != 0 and W_z != 0:
					#	num_puntos[new_i,new_j,new_k] += 1
#rho = num_puntos*rho
rho = (1.0/(delta_x*delta_y*delta_z))*rho
print("Listo")

#1b. 
#Se encuentra la transformada inversa de Fourier de phi_gorrito que sabemos que phi_gorrito = -rho_gorrito. 
#Para esto se asume que rho_gorrito = rho
print('Se comienza a construir la matriz phi. Favor esperar y no entrar en pánico')
rho_gorrito= np.fft.fftn(rho)
phi_gorrito = rho_gorrito*(-1)
phi = np.fft.ifftn(phi_gorrito)
phi = abs(phi)
print('Listo')


#1c.
print('Finalmente se crea la matriz con las fuerzas')
#La fuerza la calculamos a partir de sus componentes como sqrt(F_x^2+F_y^2+F_z^2)
#Por ejemplo, la componente en x se calcula como F_x = - dphi/dx

F_x = (phi[1:,:,:] - phi[:-1,:,:])[:,:-1,:-1]/delta_x
F_y = (phi[:,1:,:] - phi[:,:-1,:])[:-1,:,:-1]/delta_y
F_z = (phi[:,:,1:] - phi[:,:,:-1])[:-1,:-1,:]/delta_z

F_x = -1*F_x
F_y = -1*F_y
F_z = -1*F_z

F = ((F_x**2)+(F_y**2)+(F_z**2))**(0.5)
print('Listo calisto!!')
# print(force)

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

#Ahora queremos graficar en un plano 
F_proyeccion = F[:,:,0]
for i in range(1, size-1):
    F_proyeccion = F_proyeccion + F[:,:,i]

fig, axs = plt.subplots(1,2)
fig.suptitle("Comparación de contornos de la fuerza gravitacional\n y distribución de particulas", fontsize=16)
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


plt.show()
# mpl.plot()

