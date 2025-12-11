#Grafica los archivos que se generan con el tally [T-Cross] de PHITS
#Adaptado para ver las salidas de 6MeV_LiF.inp
#En archivo* poner la ruta completa al *.out que se va a graficar
#Última modificación: 10/12/2025.
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
#	print(llaves)
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

archivo = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/fuente_hispanos/blanco_LiLiF.output"

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

def adquirir_espectros_de_archivo(archivo, encabezado1: int, cant_interv: int):
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
	return reg1

corriente_Pb_a_exterior = adquirir_espectros_de_archivo(archivo, 54, 101)

#Integrales ··············
#neutrones ···
Pb_0_1_cm_n_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["neutron"], 1) 
#gammas ·····
Pb_0_1_cm_gammas_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["photon"], 1) 
#alfas ······
blanco_7Be_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["7Be"], 1) 
#electrones ······
Pb_0_1_cm_electrones_tot_salen = Particle_number_through_geometry(corriente_Pb_a_exterior["e-lower"], corriente_Pb_a_exterior["e-upper"],  corriente_Pb_a_exterior["electron"], 1) 

print("Nº de neutrones que salen por proton emitido ", round(Pb_0_1_cm_n_tot_salen,10))

print("Nº de gammas que salen por proton emitido ", round(Pb_0_1_cm_gammas_tot_salen,10))

print("Nº de 7Be que salen por proton emitido ", round(blanco_7Be_tot_salen,10))

print("Nº de electrones que salen por proton emitido ", round(Pb_0_1_cm_electrones_tot_salen,10))

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
fig.canvas.manager.set_window_title('Particulas generadas en el blanco')
title_ylabel = 'Corriente [partíc/MeV/p$_{emit}$]'
title_xlabel = 'Energy [MeV]'

for ax in axs.flat:
	ax.grid(color='gray', axis='both')
	ax.ticklabel_format(axis = 'y', style = 'sci', useMathText=True, scilimits = (-0,0))

#neutrones ··············
axs[0, 0].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['neutron'], [x*y for x, y in zip(corriente_Pb_a_exterior['neutron'], corriente_Pb_a_exterior['neutronr.err'])], marker = '<' , ls = 'None', label =  r'$neutrones$', color = 'tab:pink')#
axs[0, 0].set_yscale('log')
axs[0,0].set_ylabel(title_ylabel)
axs[0,0].legend(loc=1)
#axs[0,0].set_xlim(1e-6, 1.5e-1)
axs[0,0].set_ylim(1e-8, 1e-5)

#Fotones ··············
axs[1, 0].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['photon'], [x*y for x, y in zip(corriente_Pb_a_exterior['photon'], corriente_Pb_a_exterior['photonr.err'])], marker = '<' , ls = 'None', label =  r'$\gamma$', color = 'tab:brown')#
axs[1, 0].set_yscale('log')
axs[1,0].set_ylabel(title_ylabel)
axs[1,0].set_xlabel(title_xlabel)
axs[1,0].legend(loc=1)
#axs[1,0].set_xlim(5e-2, 1e-1)
#axs[1,0].set_ylim(1e-6, 1e-1)


#7Be ···············
axs[0, 1].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['7Be'], [x*y for x, y in zip(corriente_Pb_a_exterior['7Be'], corriente_Pb_a_exterior['7Ber.err'])], marker = '<', ls = 'None', label =  r'$ ^{7}$ Be', color = 'tab:olive')#
axs[0,1].legend(loc=1)
#axs[0,1].set_ylim(1e-8, 1e-5)

#Electrones ···············
axs[1, 1].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['electron'], [x*y for x, y in zip(corriente_Pb_a_exterior['electron'], corriente_Pb_a_exterior['electronr.err'])], marker = '<', ls = 'None', label =  r'$e^{-}$', color = 'tab:blue')#
axs[1,1].set_xlabel(title_xlabel)
axs[1,1].legend(loc=1)
axs[1,1].set_ylim(1e-8, 5e-7)

#axs[1,0].set_xlabel(lines[231].split(':')[1])
#axs[1, 1].errorbar(corriente_Pb_a_exterior['e_mean'], corriente_Pb_a_exterior['positron'], [x*y for x, y in zip(corriente_Pb_a_exterior['positron'], corriente_Pb_a_exterior['positronr.err'])], marker = '<' , markersize = 8 , ls = 'None', label =  r'$e^{+}$', color = 'tab:red')#
#axs[1,1].set_xlabel(lines[231].split(':')[1])
#axs[1,1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

#for ax in axs.flat:
#	ax.legend(loc=1)#ncol=3

plt.savefig("/home/eliana/phits/Simulaciones/Quenching_Sevilla/corriente_particulas_secundarias_y_primarias_fuera_blanco_7Li.png")
plt.tight_layout()
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
'''
	#corriente = {x+llaves[idx-1]: [] for idx, x in enumerate(llaves) if (idx % 2 == 0) and (idx > 2)}
	#corriente = {x: [] for x in llaves}

#print(list(corriente.get('allr.err'))[:100])#
#e_mean = list(map(lambda x,y: (x+y)*0.5, e_upper, e_lower))
