#Grafica los archivos que se generan con el tally [T-Deposit] de PHITS
#Adaptado para ver las salidas de Si_Al_Acero_Am-Be_isotropa_cilindrica.inp
#En archivo poner la ruta completa al *.out que se va a graficar
#Última modificación: 26/09/2025.

import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import re 
import matplotlib.pylab as pylab

#Valores globales de los parametros estilisticos de las figuras
params = {'legend.fontsize': 16, 'figure.figsize': (13, 7), 'axes.labelsize': 16,'axes.titlesize':16,
		'xtick.labelsize':16,'ytick.labelsize':16,'xtick.direction':'in','ytick.direction':'in', 'lines.markersize': 8}#, 
pylab.rcParams.update(params)
#plt.rcParams.update({'text.usetex': True})
#plt.rc('text', usetex=True)

#Contenido del archivo out a listas
def energy_histo_to_list(h_le: list, h_he: list, desde: int, hasta: int) -> list:
	for fila in lines[desde:hasta]:
		columnas = fila.split()
		h_le.append(float(columnas[0]))
		h_he.append(float(columnas[1]))

def histo_to_list(h_altura: list, r_error: list, col_h: int, col_r_e: int , desde: int, hasta: int, factor: float) -> list:
	for fila in lines[desde:hasta]:
		columnas = fila.split()
		h_altura.append(float(columnas[col_h])*factor)#convierto nanosegundos a segundos
		r_error.append(float(columnas[col_r_e]))
	
	return [x*y for x, y in zip(h_altura, r_error)]

#Energía total depositada
def total_deposit_energy_1(e_l: list, e_u: list, h_content: list) -> float:
	return sum(map(lambda x, y, z: (y-x)*z, e_l, e_u, h_content))

def total_deposit_energy(h_content: list) -> float:
	return sum(h_content)

def angulo_solido_fuente_disco(R: float, D: float) -> float:
	return 2*np.pi*(1-D/np.sqrt(R**2+D**2))

archivo = "deposit_Si_670microm_n_Am-Be_isotropo_camara_acero_caja_Al.out"

#Guardo en una lista el contenido del archivo. Modificar este para que localice las filas en las que aparece este texto: #   no. =    1   reg = 100 - 105
try: 
	
	with open(archivo, 'r', encoding='utf-8') as f:
            lines = f.readlines()#queda todo el archivo guardado acá

except Exception as e:
    print(f"Error: {e}")

#print(lines[278:281])
#print("Cantidad de filas a procesar : ", len(lines))

e_lower = []
e_upper = []
energy_histo_to_list(e_lower, e_upper, 59, 160)
e_mean = [(x+y)*0.5 for x, y in zip(e_upper,e_lower)] #Centro del intervalo de clases
todas = []
todas_r_err = []
todas_abs_err = histo_to_list(todas, todas_r_err, 2, 3, 59, 160, 1)#convierto nanosegundos a segundos
#Inicio gráfico
fig, ax = plt.subplots()
#ax.errorbar(e_mean, todas, todas_abs_err, marker = '^' , markersize = 8 , ls = 'None', label =  'Todas las interacciones \n' + 'Integral = '+ f'{total_deposit_energy_1(e_lower,e_upper,todas):1.2}' + ' $1/n_{i}$', color = 'darkmagenta')
ax.errorbar(e_mean, todas, todas_abs_err, marker = '^' , markersize = 8 , ls = 'None', label =  'Todas las interacciones \n' + 'Integral = '+ f'{total_deposit_energy(todas):1.2}' + ' $int/n_{e}$', color = 'darkmagenta')
Si = []
Si_r_err = []
Si_abs_err = histo_to_list(Si, Si_r_err, 4, 5, 59, 160, 1)#convierto nanosegundos a segundos
#ax.errorbar(e_mean, todas, Si_abs_err, marker = '^' , markersize = 8 , ls = 'None', label =  'Si \n' + 'Integral = ' + f'{total_deposit_energy_1(e_lower,e_upper,Si):1.2}' + ' $1/n_{i}$', color = 'dodgerblue')
ax.errorbar(e_mean, todas, Si_abs_err, marker = '^' , markersize = 8 , ls = 'None', label =  'Si \n' + 'Integral = '+ f'{total_deposit_energy(Si):1.2}' + ' $int/n_{e}$', color = 'dodgerblue')
neutron = []
neutron_r_err = []
neutron_abs_err = histo_to_list(neutron, neutron_r_err, 6, 7, 59, 160, 1)#convierto nanosegundos a segundos
#ax.errorbar(e_mean, neutron, neutron_abs_err, marker = '^' , markersize = 8 , ls = 'None', label =  'neutron \n' + 'Integral = '+ f'{total_deposit_energy_1(e_lower,e_upper,neutron):1.2}' + ' $1/n_{i}$', color = 'darkorange')
ax.errorbar(e_mean, neutron, neutron_abs_err, marker = '^' , markersize = 8 , ls = 'None', label =  'neutron \n' + 'Integral = '+ f'{total_deposit_energy(neutron):1.2}' + ' $int/n_{e}$', color = 'darkorange')
alfa = []
alfa_r_err = []
alfa_abs_err = histo_to_list(alfa, alfa_r_err, 8, 9, 59, 160, 1)#convierto nanosegundos a segundos
#ax.errorbar(e_mean, alfa, alfa_abs_err, marker = '^' , markersize = 8 , ls = 'None', label =  '$\\alpha$ \n' + 'Integral = '+ f'{total_deposit_energy_1(e_lower,e_upper,alfa):1.2}' + ' $1/n_{i}$', color = 'magenta')
ax.errorbar(e_mean, alfa, alfa_abs_err, marker = '^' , markersize = 8 , ls = 'None', label =  '$\\alpha$ \n' + 'Integral = '+ f'{total_deposit_energy(alfa):1.2}' + ' $int/n_{e}$', color = 'magenta')

#print('energy = ', e_lower[len(e_lower)-1], 'all = ', todas[len(e_lower)-1], 'Si = ', Si[len(e_lower)-1], 'n = ', neutron[len(e_lower)-1] , 'alfa = ', alfa[len(e_lower)-1])
print('Integral: suma(contenido del intervalo * ancho del intervalo)\n' + 'Todas las interacciones = ' + f'{total_deposit_energy_1(e_lower,e_upper,todas):1.2}  \n ' + 'Si :' + f'{total_deposit_energy_1(e_lower,e_upper,Si):1.2}  \n ' + 'neutron :' + f'{total_deposit_energy_1(e_lower,e_upper,neutron):1.2}  \n ' + 'alfa :' + f'{total_deposit_energy_1(e_lower,e_upper,alfa):1.2}  \n ')
print('Integral: suma(contenido del intervalo) \n' + 'Todas las interacciones = ' + f'{total_deposit_energy(todas):1.2}  \n ' + 'Si :' + f'{total_deposit_energy(Si):1.2}  \n ' + 'neutron :' + f'{total_deposit_energy(neutron):1.2}  \n ' + 'alfa :' + f'{total_deposit_energy(alfa):1.2}  \n ')


# Estética Gráfico
plt.xlabel('Energía depositada [MeV]')#lines[53].split(':')[1])
plt.ylabel('Interacciones [Nº/n$_{emitidos}$]')#lines[54].split(':')[1]
plt.title("Neutrones de Am-Be. Si encapsulado en Al dentro de cámara de acero ", fontsize=16)
plt.grid(True, linestyle='--', alpha=0.5)
#plt.yscale('log')
#plt.xscale('log')
#plt.ylim(1e-9, 1e-4)
#plt.gca().ticklabel_format(axis = 'y', style = 'sci')
plt.legend(loc = 'upper right', ncol=2)
plt.tight_layout()
plt.savefig("/home/eliana/Documentos/Neutrones/energia_depositada_sistema_CAB.png")
plt.show()
