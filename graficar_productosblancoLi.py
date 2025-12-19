#Grafica los archivos que se generan con el tally [T-Cross] de PHITS
#Adaptado para ver las salidas de productosblancoLi.inp
#En archivo* poner la ruta completa al *.out que se va a graficar
#Última modificación: 19/12/2025.
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import re 
import matplotlib.pylab as pylab
from itertools import islice
from matplotlib.ticker import ScalarFormatter

#Valores globales de los parametros estilisticos de las figuras
params = {'legend.fontsize': 12, 'figure.figsize': (12, 7), 'axes.labelsize': 13,'axes.titlesize':8,
		'xtick.labelsize':16,'ytick.labelsize':16,'xtick.direction':'in','ytick.direction':'in', 'lines.markersize': 5}#, 
pylab.rcParams.update(params)

#······················ FUNCIONES ·······················································································
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

def leer_archivo_de_2_columnnas(archivo):
	
	col1 = []
	col2 = []

	with open(archivo, 'r', encoding='utf-8') as f:
		
		next(f)

		for line in f:
			#print(line)
			try:
				c1, c2 = line.split()
				col1.append(float(c1))
				col2.append(float(c2))
			except ValueError as e:
				pass
				#c1 = line.split()
				#col1.append(float(c1[0]))
				
	return col1, col2
	
# FIN FUNCIONES ·······················································································
espectro_hispanos = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/n_HISPANOS.inp"
#archivo = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/fuente_hispanos/productos_de_reaccion/product_eng.out"
archivo2 = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/fuente_hispanos/productos_de_reaccion/product_eng_2.out"#usando modelos nucleares
archivo3 = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/fuente_hispanos/productos_de_reaccion/product_eng_3.out"#usando librerías 
#archivo3 = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/fuente_hispanos/blanco_LiLiF_2.output"

ene_hispanos, intensidad_hispanos_ua = leer_archivo_de_2_columnnas(espectro_hispanos)
productos_pLiF_model = adquirir_espectros_de_archivo(archivo2, 48, 51)
productos_pLiF_librerias = adquirir_espectros_de_archivo(archivo3, 48, 51)
#productos_pLiF = adquirir_espectros_de_archivo(archivo, 58, 101)#55
#productos_pLiF = adquirir_espectros_de_archivo(archivo, 74, 201)

#print("Energia ", ene_hispanos, "intensidad = " , intensidad_hispanos)
print("HISPANOS cantidad de intervalos = ", len(intensidad_hispanos_ua))
#Integrales ··············
#neutrones ···
neutron_integ_model = Particle_number_through_geometry(productos_pLiF_model["e-lower"][1:len(intensidad_hispanos_ua)], productos_pLiF_model["e-upper"][1:len(intensidad_hispanos_ua)],  productos_pLiF_model["neutron"][1:len(intensidad_hispanos_ua)], 1) 
neutron_integ_lib = Particle_number_through_geometry(productos_pLiF_librerias["e-lower"][1:len(intensidad_hispanos_ua)], productos_pLiF_librerias["e-upper"][1:len(intensidad_hispanos_ua)],  productos_pLiF_librerias["neutron"][1:len(intensidad_hispanos_ua)], 1) 
intensidad_hispanos_integ = sum(intensidad_hispanos_ua)*0.01
#Renormalizo el espectro del paper de HISPANOS
intensidad_hispanos = [i*neutron_integ_lib/intensidad_hispanos_integ for i in intensidad_hispanos_ua]
#print(type(intensidad_hispanos[0]))
#print(type(neutron_integ_lib))
#gammas ·····
gammas_salen = Particle_number_through_geometry(productos_pLiF_model["e-lower"], productos_pLiF_model["e-upper"],  productos_pLiF_model["photon"], 1) 

print("Integral espectro HISPANOS en unidades arbitrarias = ", round(intensidad_hispanos_integ,10))
print("Nº de neutrones de 10 a 120 keV por proton emitido MODELOS = ", round(neutron_integ_model,10))
print("Nº de neutrones de 10 a 120 keV  por proton emitido JENDL-4 = ", round(neutron_integ_lib,10))
#print("Nº de gammas que salen por proton emitido ", round(gammas_salen,10))
#print(sum(productos_pLiF_model["photon"])*0.005)

fig, axs = plt.subplots(1, 2, figsize=(15, 10), sharey = False, sharex = True)
fig.canvas.manager.set_window_title('Particulas generadas en el blanco')
title_ylabel = r'Corriente [partic/MeV/cm$^{3}$/p$_{emit}$]'
title_ynlabel = r'Neutrones [Nº/MeV/cm$^{3}$/p$_{emit}$]'
title_yglabel = r'$\gamma$ [Nº/MeV/p$_{emit}$]'
title_xlabel = 'Energy [MeV]'

for ax in axs.flat:
	ax.grid(color='gray', axis='both')
	ax.ticklabel_format(axis = 'y', style = 'sci', useMathText=True, scilimits = (-0,0))

#neutrones ··············
axs[0].errorbar(productos_pLiF_model['e_mean'], productos_pLiF_model['neutron'], [x*y for x, y in zip(productos_pLiF_model['neutron'], productos_pLiF_model['neutronr.err'])], marker = '<' , ls = 'None', label =  'Modelos de reacciones nucleares', color = 'tab:pink')#
axs[0].errorbar(productos_pLiF_librerias['e_mean'], productos_pLiF_librerias['neutron'], [x*y for x, y in zip(productos_pLiF_librerias['neutron'], productos_pLiF_librerias['neutronr.err'])], marker = 'o' , ls = 'None', label =  r'$\sigma$ en JENDL-4.0', color = 'tab:olive')#
axs[0].scatter(ene_hispanos, intensidad_hispanos, s = 200, marker = '*', label = 'CNA HISPANOS', color = 'tab:blue')
axs[0].set_yscale('log')
axs[0].set_ylabel(title_ynlabel)
axs[0].set_xlabel(title_xlabel)
axs[0].legend(loc=4)
#axs[0,0].set_xlim(1e-6, 1.5e-1)
axs[0].set_ylim(1e-8, 3e-5)

#Fotones ··············
axs[1].errorbar(productos_pLiF_model['e_mean'], productos_pLiF_model['photon'], [x*y for x, y in zip(productos_pLiF_model['photon'], productos_pLiF_model['photonr.err'])], marker = '<' , ls = 'None', label =  'Modelos', color = 'tab:brown')#
axs[1].errorbar(productos_pLiF_librerias['e_mean'], productos_pLiF_librerias['photon'], [x*y for x, y in zip(productos_pLiF_librerias['photon'], productos_pLiF_librerias['photonr.err'])], marker = 'o' , ls = 'None', label =  'JENDL-4.0', color = 'tab:olive')#
axs[1].set_yscale('log')
axs[1].set_ylabel(title_yglabel)
axs[1].set_xlabel(title_xlabel)
axs[1].set_ylim(1e-6, 5e-4)
axs[1].legend(loc=1)

#plt.savefig("/home/eliana/phits/Simulaciones/Quenching_Sevilla/corriente_neutrones_y_fotones_fuera_blanco_7Li_2.png")
plt.savefig("/home/eliana/phits/Simulaciones/Quenching_Sevilla/n_g_producidos_por_p_Li-LiF.png")
plt.tight_layout()
plt.show()

# END ------------------------------------------------------------------------------------------------------------------------


#Adevertencias cuando usé las librería de datos nucleares así: dmax(protones)  =  dmax(neutrones) = 150.0 MeV, dmax(fotones) = 1e3 MeV

#*** Warning: emin( 1) is adjusted to 1.0000000D-03 by esmin
#e-mode dose not work well when dmax(2) is above 20 MeV.
#   9019.51h
#These nuclear data libraries are missing. Physical models are used for corresponding nuclear reactions.
#   3006.51c
#   3007.51c
#   9019.51c
#These nuclear data libraries are missing.  JENDL-4.0 is used for these nuclei up to 20MeV.
