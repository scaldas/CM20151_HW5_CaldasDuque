import numpy as np 

x = np.linspace(0,20,1000)
#print(x)

y = x**2
#print(y)

dx = x[1] - x[0]
#print(dx)s

print(np.gradient(y, dx))

der = y[1:] - y[:-1]
der = der/dx

print(der)