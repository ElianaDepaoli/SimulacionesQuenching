#!/bin/python3
#La fila de arriba es necesaria para que sean localizadas las librerías que se importan a continuación
#Grafica los archivos que se generan con el tally [T-Cross] de PHITS
#Adaptado para ver las salidas de Si_Al_Acero_Am-Be_isotropa_cilindrica.inp
#Ver al final cómo usarlo
#Última modificación: 23/10/2025.
import __main__
import sys
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import re 
import matplotlib.pylab as pylab

#Valores globales de los parametros estilisticos de las figuras
params = {'legend.fontsize': 17, 'figure.figsize': (12, 7), 'axes.labelsize': 16,'axes.titlesize':16,
		'xtick.labelsize':16,'ytick.labelsize':16,'xtick.direction':'in','ytick.direction':'in', 'lines.markersize': 8}#, 
pylab.rcParams.update(params)
#plt.rcParams.update({'text.usetex': True})
#plt.rc('text', usetex=True)

#Contenido del archivo out a listas
def energy_histo_to_list(lines: list, h_le: list, h_he: list, desde: int, hasta: int) -> list:
	for fila in lines[desde:hasta]:
		columnas = fila.split()
		h_le.append(float(columnas[0]))
		h_he.append(float(columnas[1]))

def histo_to_list(lines: list, h_altura: list, r_error: list , desde: int, hasta: int, area: float) -> list:
	for fila in lines[desde:hasta]:
		columnas = fila.split()
		h_altura.append(float(columnas[2])/area)
		r_error.append(float(columnas[3]))
	
	return [x*y for x, y in zip(h_altura, r_error)]

#Número total de neutrones que pasan por la geometría
def Neutron_number_through_geometry(e_l: list, e_u: list, h_content: list, area: float) -> float:
	return sum(map(lambda x, y, z: (y-x)*z, e_l, e_u, h_content))/area

def angulo_solido_fuente_disco(R: float, D: float) -> float:
	return 2*np.pi*(1-D/np.sqrt(R**2+D**2))

def angulo_solido_fuente_rectangulo(a:float, b:float, D: float) -> float:
	return 4*np.arctan(a*b/D/np.sqrt(a**2+b**2+D**2))

#archivo = "/home/eliana/phits/Simulaciones/Neutrones_CAB/camara_acero/resultados/corriente.output"

def main (archivo, figura_out, low_en_bin, upper_en_bin):
#Guardo en una lista el contenido del archivo. Modificar este para que localice las filas en las que aparece este texto: #   no. =    1   reg = 100 - 105
	try: 
		
		with open(archivo, 'r', encoding='utf-8') as f:
	            lines = f.readlines()#queda todo el archivo guardado acá

	except Exception as e:
	    print(f"Error: {e}")

	#print("Cantidad de filas a procesar : ", len(lines))
	offset = 121
	e_lower = []
	e_upper = []
	n_fuente = []
	n_fuente_err = []
	n_acero = []
	n_acero_err = []
	n_Al = []
	n_Al_err = []
	n_vuelven_exterior = []
	n_vuelven_exterior_err = []

	altura_ext_camisa = 21.4+2*1.2
	diametro_ext_camisa = 22 							#[cm]
	diametro_int_camisa = 21.4						    #[cm]
	D_fuente_tapa_ext_acero = 1.00000E-9 				#[cm]
	D_fuente_tapa_int_acero = 1.00000E-9 + 1.2			#[cm]
	D_fuente_detector = 17.217							#[cm]
	area_tapa_ext_camisa_acero = np.pi*(diametro_ext_camisa/2)**2    #[cm2]
	area_tapa_int_camisa_acero = np.pi*(diametro_int_camisa/2)**2    #[cm2]
	area_lateral_ext_camisa_acero = np.pi*diametro_ext_camisa*altura_ext_camisa    #[cm2]
	area_caja_Al = 16.5*10.5                               #[cm2]
	a_detector = 9.225 									#[cm]
	b_detector = 2.352 									#[cm]
	area_detector_Si = a_detector*b_detector            #[cm2]
	print("area_tapa_ext_camisa_acero = ", area_tapa_ext_camisa_acero,"area_tapa_int_camisa_acero = ", area_tapa_int_camisa_acero, "area_caja_Al = ", area_caja_Al, "area_detector_Si = ", area_detector_Si)

	energy_histo_to_list(lines,e_lower, e_upper, low_en_bin, upper_en_bin)
	e_mean = [(x+y)*0.5 for x, y in zip(e_upper,e_lower)]
	#e_mean = list(map(lambda x,y: (x+y)*0.5, e_upper, e_lower))

	#Fuente ··············no. =    1   reg = 101 - 107 #····················································
	n_fuente_abs_error = histo_to_list(lines, n_fuente, n_fuente_err, low_en_bin, upper_en_bin, 1) #   area_tapa_ext_camisa_acero
	#print('first energy bin = ', e_lower[0], '  ' , 'last energy bin = ',e_lower[len(e_lower)-1], 'Nº energy bins = ', len(e_lower))
	#print('size data = ', len(n_fuente), 'size error = ', len(n_fuente_abs_error))
	fuente_n_tot = Neutron_number_through_geometry(e_lower, e_upper, n_fuente, 1)
	plt.errorbar(e_mean, n_fuente, n_fuente_abs_error, marker = '^' , markersize = 8 , ls = 'None', label =  'Dewar - Acero\n' + '$\\epsilon_{}$ = '+ f'{fuente_n_tot:1.2}', color = 'darkmagenta')#Dewar - Acero #107
	#print('contenido intervalo = ', n_fuente, 'error relativo = ', n_fuente_err)
	#print('error absoluto = 	' , n_fuente_abs_error)
	#Al interior de la camara de vacio luego de pasar por el acero ···· no. =    2   reg = 107 - 106··········
	n_acero_abs_error = histo_to_list(lines, n_acero, n_acero_err, low_en_bin + offset, upper_en_bin + offset, 1)#area_tapa_int_camisa_acero
	acero_n_tot_salen = Neutron_number_through_geometry(e_lower, e_upper,  n_acero, 1) 
	plt.errorbar(e_mean, n_acero, n_acero_abs_error, marker = 's' , ls = 'None', label = 'Dewar - Interior\n' + '$\\epsilon_{}$ =' + f'{acero_n_tot_salen:1.2}', color = 'darkorange')#Dewar - Interior #106

	# Llegan al Si luego de pasar por el Al ·······no. =    3   reg = 104 - 105 ····························
	n_Al_abs_error = histo_to_list(lines, n_Al, n_Al_err, low_en_bin + 2*offset, upper_en_bin + 2*offset, 1)
	Al_n_tot_salen =  Neutron_number_through_geometry(e_lower, e_upper,  n_Al, 1)
	print('Nº eventos en el detector = ', Al_n_tot_salen, '[nt/ne]')
	plt.errorbar(e_mean, n_Al, n_Al_abs_error, marker = '8' , ls = 'None', label = 'Detector\n' + '$\\epsilon_{}$  = '+ f'{Al_n_tot_salen:1.3}', color = 'dodgerblue')

	# Estética Gráfico
	plt.xlabel('Energy [MeV]')#lines[53].split(':')[1]
	plt.ylabel('Corriente [n/MeV/n$_{emitidos}$]')#lines[54].split(':')[1]
	plt.title("Neutrones provenientes de una fuente cilíndrica a 96.5 cm del lateral del Dewar", fontsize=16)
	plt.grid(True, linestyle='--', alpha=0.5)
	plt.yscale('log')#linear
	plt.ylim(max(min(n_Al),1e-9), max(n_fuente)*1.2)
	#plt.xlim(min(e_mean)*.5, max(e_upper)*1.1)
	#plt.gca().ticklabel_format(axis = 'y', style = 'sci')
	leg = plt.legend(loc = 'lower left', ncol=3, title = 'Fracción de n transmitidos \n [n$_{transmitidos}$/n$_{emitidos}$]') #best
	leg.get_title().set_fontsize('15')
	plt.tight_layout()
	#plt.text(8, 9e-2, '$f_{calc}^{tapa}$ = ' + f'{angulo_solido_fuente_disco(diametro_ext_camisa/2, D_fuente_tapa_ext_acero)/4/np.pi :1.2}', fontsize=18 , color = 'darkmagenta')
	#plt.text(8, 3e-3, r'$f_{calc}^{interior \quad camara}$ = ' + f'{angulo_solido_fuente_disco(diametro_int_camisa/2, D_fuente_tapa_int_acero)/4/np.pi :1.2}', fontsize=18 , color = 'darkorange')
	#plt.text(8, 1e-3, r'$f_{calc}^{Detector}$ = ' + f'{angulo_solido_fuente_rectangulo(a_detector, b_detector, D_fuente_detector)/4/np.pi :1.2}', fontsize=18 , color = 'dodgerblue')
	#plt.text(2, 1e-4, 'Fracción de n que llegan al detector = ' + f'{acero_n_tot_salen:1.2e}', fontsize=16, color = 'darkorange')
	plt.savefig(figura_out)
	plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print(f"Modo de uso: {sys.argv[0]} ruta/completa/al/archivo/a/procesar [inicio_bin] [fin_bin] /ruta/y/nombre/figura/salida")
        print(f"Ejemplo: {sys.argv[0]} /ruta/al/archivo.output 58 158")
        sys.exit(1)
        
    archivo = sys.argv[1]
    if len(sys.argv) < 3:
    	print("Usando valores por defecto para los bins de energía: 58, 158")
    	figura_out = "/home/eliana/Documentos/Neutrones/corriente_medicion_Skipper_CAB_fuente_cilindrica.png"
    	main(archivo, figura_out, 57, 157)
    else:
    	figura_out = sys.argv[4]
    	inicio_bin = int(sys.argv[2])
    	fin_bin = int(sys.argv[3])
    	main(archivo, figura_out , inicio_bin, fin_bin)
    	#print(sys.argv[2], " ------- ", sys.argv[3])







# END ------------------------------------------------------------------------------------------------------------------------

# Salen del acero al vacío exterior ·········no. =    4   reg = 107 - 101 ······························
'''n_vuelven_exterior_abs_error = histo_to_list(lines, n_vuelven_exterior, n_vuelven_exterior_err, 421, 521, 1) #(area_lateral_ext_camisa_acero+area_tapa_ext_camisa_acero)
vuelven_exterior_n_tot =  Neutron_number_through_geometry(e_lower, e_upper,  n_vuelven_exterior_err, 1)
plt.errorbar(e_mean, n_vuelven_exterior, n_vuelven_exterior_abs_error, marker = '^' , ls = 'None', label = 'Acero al exterior vacío.\n' + 'f = '+ f'{vuelven_exterior_n_tot:1.2}' + ' $n_{t}/n_{e}$', color = 'magenta')
'''