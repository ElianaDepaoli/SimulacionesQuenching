#Grafica los archivos que se generan con el tally [T-Cross] de PHITS
#Adaptado para ver las salidas de n_uniforme_Pb.inp
#En archivo* poner la ruta completa al *.out que se va a graficar
#Última modificación: 03/12/2025.
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import re 
import matplotlib.pylab as pylab
from itertools import islice
from matplotlib.ticker import ScalarFormatter

#Valores globales de los parametros estilisticos de las figuras
params = {'legend.fontsize': 12, 'figure.figsize': (12, 7), 'axes.labelsize': 13,'axes.titlesize':8,
		'xtick.labelsize':16,'ytick.labelsize':16,'xtick.direction':'in','ytick.direction':'in', 'lines.markersize': 3}#, 
pylab.rcParams.update(params)

#Contenido del archivo out a diccionario
def histo_to_dicc(encabezado: int, cant_interv: int, lines: list) -> dict:
	#Diccionario cuyas llaves son los nombres en el encabezado y cuyos items son listas vacías
	llaves = lines[encabezado].split()
	llaves.pop(0)
	#print(llaves)
	corriente = {x: [] for x in llaves}#(idx % 2 != 0) and  
	corriente.pop('r.err')

	for idx, x in enumerate(llaves):
		if (idx % 2 != 0) and (idx > 2):
			corriente[llaves[idx-1]+x] = [] 
	#print(corriente.keys())
	# ·················································
	#Lleno las listas con los espectros
	for fila in lines[encabezado+1:encabezado+1+cant_interv]:
		columnas = fila.split()
		for idx, x in enumerate(columnas):
			if idx > 1 and (idx % 2 == 0):
				corriente[llaves[idx]].append(float(columnas[idx]))
			elif idx < 2:
				corriente[llaves[idx]].append(float(columnas[idx]))
			elif idx > 1 and (idx % 2 != 0):
				corriente[llaves[idx-1]+llaves[idx]].append(float(columnas[idx]))

	return corriente

#Número total de partículas que pasan por la geometría
def Particle_number_through_geometry(e_l: list, e_u: list, h_content: list, area: float) -> float:
	return sum(map(lambda x, y, z: (y-x)*z, e_l, e_u, h_content))/area

def angulo_solido_fuente_disco(R: float, D: float) -> float:
	return 2*np.pi*(1-D/np.sqrt(R**2+D**2))

def angulo_solido_fuente_rectangulo(a:float, b:float, D: float) -> float:
	return 4*np.arctan(a*b/D/np.sqrt(a**2+b**2+D**2))

archivo = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/blindaje/corriente_0_1cm.output"
archivo2 = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/blindaje/corriente_0_5cm.output"
archivo3 = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/blindaje/corriente_1_0cm.output"


def adquirir_espectros_de_archivo(archivo, encabezado1: int, encabezado2: int, cant_interv: int):
	lines = []
	#Guardo en una lista el contenido del archivo.
	try:
		with open(archivo, 'r', encoding='utf-8') as f:
			lines = f.readlines()#queda todo el archivo guardado acá

	except Exception as e:
		print(f"Error: {e}")

	#print(lines)
	reg1 = histo_to_dicc(encabezado1, cant_interv, lines)
	reg1['e_mean'] = [(x+y)*0.5 for x, y in zip(reg1['e-upper'],reg1['e-lower'])]
	reg2 = histo_to_dicc(encabezado2, cant_interv, lines)
	reg2['e_mean'] = [(x+y)*0.5 for x, y in zip(reg2['e-upper'],reg2['e-lower'])]
	return reg1, reg2

corriente_exterior_a_Pb, corriente_Pb_a_exterior = adquirir_espectros_de_archivo(archivo, 235, 1256, 1001)
corriente_exterior_a_Pb_0_5, corriente_Pb_a_exterior_0_5 = adquirir_espectros_de_archivo(archivo2, 235, 1256, 1001)
corriente_exterior_a_Pb_1_0, corriente_Pb_a_exterior_1_0 = adquirir_espectros_de_archivo(archivo3, 235, 1256, 1001)
#Integrales ··············
#neutrones ···
Pb_0_1_cm_n_tot_entran = Particle_number_through_geometry(corriente_exterior_a_Pb["e-lower"], corriente_exterior_a_Pb["e-upper"],  corriente_exterior_a_Pb["neutron"], 1)
Pb_0_1_cm_n_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["neutron"], 1) 
Pb_0_5_cm_n_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_0_5["e-lower"], corriente_Pb_a_exterior_0_5["e-upper"],  corriente_Pb_a_exterior_0_5["neutron"], 1)  
Pb_1_0_cm_n_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_1_0["e-lower"], corriente_Pb_a_exterior_1_0["e-upper"],  corriente_Pb_a_exterior_1_0["neutron"], 1)  
#gammas ·····
Pb_0_1_cm_gammas_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["photon"], 1) 
Pb_0_5_cm_gammas_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_0_5["e-lower"], corriente_Pb_a_exterior_0_5["e-upper"], corriente_Pb_a_exterior_0_5["photon"], 1)  
Pb_1_0_cm_gammas_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_1_0["e-lower"], corriente_Pb_a_exterior_1_0["e-upper"], corriente_Pb_a_exterior_1_0["photon"], 1)  
#alfas ······
Pb_0_1_cm_alfas_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["alpha"], 1) 
Pb_0_5_cm_alfas_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_0_5["e-lower"], corriente_Pb_a_exterior_0_5["e-upper"], corriente_Pb_a_exterior_0_5["alpha"], 1)  
Pb_1_0_cm_alfas_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_1_0["e-lower"], corriente_Pb_a_exterior_1_0["e-upper"], corriente_Pb_a_exterior_1_0["alpha"], 1)  
#electrones ······
Pb_0_1_cm_electrones_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["electron"], 1) 
Pb_0_5_cm_electrones_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_0_5["e-lower"], corriente_Pb_a_exterior_0_5["e-upper"], corriente_Pb_a_exterior_0_5["electron"], 1)  
Pb_1_0_cm_electrones_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_1_0["e-lower"], corriente_Pb_a_exterior_1_0["e-upper"], corriente_Pb_a_exterior_1_0["electron"], 1) 

#positrones ······
Pb_0_1_cm_positrones_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["positron"], 1) 
Pb_0_5_cm_positrones_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_0_5["e-lower"], corriente_Pb_a_exterior_0_5["e-upper"], corriente_Pb_a_exterior_0_5["positron"], 1)  
Pb_1_0_cm_positrones_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior_1_0["e-lower"], corriente_Pb_a_exterior_1_0["e-upper"], corriente_Pb_a_exterior_1_0["positron"], 1) 

print("Nº de neutrones que entran por neutron emitido", round(Pb_0_1_cm_n_tot_entran, 5))
print("Nº de neutrones que salen por neutron emitido 0.1 cm de Pb", round(Pb_0_1_cm_n_tot_salen,5))
print("Nº de neutrones que salen por neutron emitido 0.5 cm de Pb", round(Pb_0_5_cm_n_tot_salen, 5))
print("Nº de neutrones que salen por neutron emitido 1.0 cm de Pb", round(Pb_1_0_cm_n_tot_salen,5))

print("Nº de gammas que salen por neutron emitido 0.1 cm de Pb", round(Pb_0_1_cm_gammas_tot_salen,8))
print("Nº de gammas que salen por neutron emitido 0.5 cm de Pb", round(Pb_0_5_cm_gammas_tot_salen,8))
print("Nº de gammas que salen por neutron emitido 1.0 cm de Pb", round(Pb_1_0_cm_gammas_tot_salen,8))

print("Nº de alfas que salen por neutron emitido 0.1 cm de Pb", round(Pb_0_1_cm_alfas_tot_salen,8))
print("Nº de alfas que salen por neutron emitido 0.5 cm de Pb", round(Pb_0_5_cm_alfas_tot_salen,8))
print("Nº de alfas que salen por neutron emitido 1.0 cm de Pb", round(Pb_1_0_cm_alfas_tot_salen,8))

print("Nº de electrones que salen por neutron emitido 0.1 cm de Pb", round(Pb_0_1_cm_electrones_tot_salen,8))
print("Nº de electrones que salen por neutron emitido 0.5 cm de Pb", round(Pb_0_5_cm_electrones_tot_salen,8))
print("Nº de electrones que salen por neutron emitido 1.0 cm de Pb", round(Pb_1_0_cm_electrones_tot_salen,8))

print("Nº de positrones que salen por neutron emitido 0.1 cm de Pb", round(Pb_0_1_cm_positrones_tot_salen,8))
print("Nº de positrones que salen por neutron emitido 0.5 cm de Pb", round(Pb_0_5_cm_positrones_tot_salen,8))
print("Nº de positrones que salen por neutron emitido 1.0 cm de Pb", round(Pb_1_0_cm_positrones_tot_salen,8))

#Guardo en una lista el contenido de un archivo. Modificar este para que localice las filas en las que aparece este texto: #   no. =    1   reg = 100 - 105
'''
try: 
	
	with open(archivo, 'r', encoding='utf-8') as f:
            lines = f.readlines()#queda todo el archivo guardado acá

except Exception as e:
    print(f"Error: {e}")

corriente_exterior_a_Pb = histo_to_dicc(235, 1001)
corriente_exterior_a_Pb['e_mean'] = [(x+y)*0.5 for x, y in zip(corriente_exterior_a_Pb['e-upper'],corriente_exterior_a_Pb['e-lower'])]
#print(corriente_exterior_a_Pb.keys())
corriente_Pb_a_exterior = histo_to_dicc(1256, 1001)
corriente_Pb_a_exterior['e_mean'] = [(x+y)*0.5 for x, y in zip(corriente_exterior_a_Pb['e-upper'],corriente_exterior_a_Pb['e-lower'])]
#print(corriente_Pb_a_exterior.keys())
'''
fig, axs = plt.subplots(2, 2, figsize=(15, 10), sharey = False, sharex = True)
fig.canvas.manager.set_window_title('Neutrones con distribucion de energia uniforme contra plomo')
title_ylabel = 'Corriente [n/MeV/n$_{emitidos}$]'
title_xlabel = 'Energy [MeV]'

for ax in axs.flat:
	ax.grid(color='gray', axis='both')
	ax.ticklabel_format(axis = 'y', style = 'sci', useMathText=True, scilimits = (-1,1))

#neutrones ··············
axs[0, 0].errorbar(corriente_Pb_a_exterior_1_0['e_mean'], corriente_Pb_a_exterior_1_0['neutron'], [x*y for x, y in zip(corriente_Pb_a_exterior_1_0['neutron'], corriente_Pb_a_exterior_1_0['neutronr.err'])], marker = 's', ls = 'None', label =  r'$n_{1.0 cm}$', color = 'tab:cyan')#
axs[0, 0].errorbar(corriente_Pb_a_exterior_0_5['e_mean'], corriente_Pb_a_exterior_0_5['neutron'], [x*y for x, y in zip(corriente_Pb_a_exterior_0_5['neutron'], corriente_Pb_a_exterior_0_5['neutronr.err'])], marker = 'v', ls = 'None', label =  r'$n_{0.5 cm}$', color = 'tab:olive')#
axs[0, 0].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['neutron'], [x*y for x, y in zip(corriente_Pb_a_exterior['neutron'], corriente_Pb_a_exterior['neutronr.err'])], marker = '<' , ls = 'None', label =  r'$n_{0.1 cm}$', color = 'tab:pink')#
axs[0, 0].set_yscale('log')
axs[0,0].set_ylabel(title_ylabel)
axs[0,0].set_xlim(1e-6, 1.5e-1)
axs[0,0].legend(loc=1)
axs[0,0].set_ylim(5e0, 2e1)

#Fotones ··············
#axs[0, 1].errorbar(corriente_exterior_a_Pb['e_mean'], corriente_exterior_a_Pb['photon'], [x*y for x, y in zip(corriente_exterior_a_Pb['photon'], corriente_exterior_a_Pb['photonr.err'])], marker = '^' , markersize = 8 , ls = 'None', label =  r'$\gamma$ exterior -> Pb', color = 'darkorange')#
axs[1, 0].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['photon'], [x*y for x, y in zip(corriente_Pb_a_exterior['photon'], corriente_Pb_a_exterior['photonr.err'])], marker = '<' , ls = 'None', label =  r'$\gamma_{0.1 cm}$', color = 'tab:pink')#
axs[1, 0].errorbar(corriente_Pb_a_exterior_0_5['e_mean'], corriente_Pb_a_exterior_0_5['photon'], [x*y for x, y in zip(corriente_Pb_a_exterior_0_5['photon'], corriente_Pb_a_exterior_0_5['photonr.err'])], marker = 'v', ls = 'None', label =  r'$\gamma_{0.5 cm}$', color = 'tab:olive')#
axs[1, 0].errorbar(corriente_Pb_a_exterior_1_0['e_mean'], corriente_Pb_a_exterior_1_0['photon'], [x*y for x, y in zip(corriente_Pb_a_exterior_1_0['photon'], corriente_Pb_a_exterior_1_0['photonr.err'])], marker = 's', ls = 'None', label =  r'$\gamma_{1.0 cm}$', color = 'tab:cyan')#
axs[1, 0].set_yscale('log')
axs[1,0].set_ylim(1e-6, 1e0)
axs[1,0].set_ylabel(title_ylabel)
axs[1,0].set_xlabel(title_xlabel)
axs[1,0].legend(loc=1)
#Fuente ·················
axs[0, 1].errorbar(corriente_exterior_a_Pb['e_mean'], corriente_exterior_a_Pb['neutron'], [x*y for x, y in zip(corriente_exterior_a_Pb['neutron'], corriente_exterior_a_Pb['neutronr.err'])], marker = '>' , ls = 'None', label =  r'$n_{fuente}$', color = 'tab:orange')# + 'f = '+ f'{fuente_n_tot:1.2}' + ' $n_{t}/n_{e}$'
axs[0,1].legend(loc=1)
#axs[0,1].set_ylim(1e-3, 2e2)
#Alfas ···············
#axs[0, 1].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['alpha'], [x*y for x, y in zip(corriente_Pb_a_exterior['alpha'], corriente_Pb_a_exterior['alphar.err'])], marker = '<', ls = 'None', label =  r'$\alpha_{0.1 cm}$', color = 'tab:pink')#
#axs[0, 1].errorbar(corriente_Pb_a_exterior_0_5['e_mean'], corriente_Pb_a_exterior_0_5['alpha'], [x*y for x, y in zip(corriente_Pb_a_exterior_0_5['alpha'], corriente_Pb_a_exterior_0_5['alphar.err'])], marker = 'v', ls = 'None', label =  r'$\alpha_{0.5 cm}$', color = 'tab:olive')#
#axs[0, 1].errorbar(corriente_Pb_a_exterior_1_0['e_mean'], corriente_Pb_a_exterior_1_0['alpha'], [x*y for x, y in zip(corriente_Pb_a_exterior_1_0['alpha'], corriente_Pb_a_exterior_1_0['alphar.err'])], marker = 's', ls = 'None', label =  r'$\alpha_{1.0 cm}$', color = 'tab:cyan')#
#axs[0,1].set_ylim(-1e-3, 1e-3)

#Electrones ···············
axs[1, 1].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['electron'], [x*y for x, y in zip(corriente_Pb_a_exterior['electron'], corriente_Pb_a_exterior['electronr.err'])], marker = '<', ls = 'None', label =  r'$e^{-}_{0.1 cm}$', color = 'tab:pink')#
axs[1, 1].errorbar(corriente_Pb_a_exterior_0_5['e_mean'], corriente_Pb_a_exterior_0_5['electron'], [x*y for x, y in zip(corriente_Pb_a_exterior_0_5['electron'], corriente_Pb_a_exterior_0_5['electronr.err'])], marker = 'v', ls = 'None', label =  r'$e^{-}_{0.5 cm}$', color = 'tab:olive')#
axs[1, 1].errorbar(corriente_Pb_a_exterior_1_0['e_mean'], corriente_Pb_a_exterior_1_0['electron'], [x*y for x, y in zip(corriente_Pb_a_exterior_1_0['electron'], corriente_Pb_a_exterior_1_0['electronr.err'])], marker = 's', ls = 'None', label =  r'$e^{-}_{1.0 cm}$', color = 'tab:cyan')#
axs[1,1].set_xlabel(title_xlabel)
axs[1,1].set_ylim(-1e-6, 4e-4)
axs[1,1].legend(loc=1)

#axs[1,0].set_xlabel(lines[231].split(':')[1])
#axs[1, 1].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['positron'], [x*y for x, y in zip(corriente_Pb_a_exterior['positron'], corriente_Pb_a_exterior['positronr.err'])], marker = '<' , markersize = 8 , ls = 'None', label =  r'$e^{+}$', color = 'tab:red')#
#axs[1,1].set_xlabel(lines[231].split(':')[1])
#axs[1,1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

#for ax in axs.flat:
#	ax.legend(loc=1)#ncol=3

plt.show()

# END ------------------------------------------------------------------------------------------------------------------------

# Estética Gráfico
'''
plt.title("Neutrones de 7Li", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
#plt.yscale('log')
plt.legend(loc = 'lower right', ncol=2)
plt.gca().ticklabel_format(axis = 'y', style = 'sci')
plt.tight_layout()
plt.savefig("/home/eliana/phits/Simulaciones/Quenching_Sevilla/corriente_n_0_1cm.png")
'''
	#corriente = {x+llaves[idx-1]: [] for idx, x in enumerate(llaves) if (idx % 2 == 0) and (idx > 2)}
	#corriente = {x: [] for x in llaves}

#print(list(corriente.get('allr.err'))[:100])#
#e_mean = list(map(lambda x,y: (x+y)*0.5, e_upper, e_lower))
