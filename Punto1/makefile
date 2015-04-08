all: plot.png 

plot.png:	plot.py forces.txt Serena-Venus.txt
	python plot.py

forces.txt: forces.py phi.txt
	python forces.py

phi.txt: phi.py rho.txt
	python phi.py

rho.txt: rho.py Serena-Venus.txt
	python rho.py

clean: 
	rm -f plot.png forces.txt phi.txt rho.txt


