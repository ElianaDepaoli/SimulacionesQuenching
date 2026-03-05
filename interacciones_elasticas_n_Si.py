import json
import matplotlib.pyplot as plt 
import numpy as np 

#Funciones ---------------------------------------------------
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


#Fin funciones ---------------------------------------------

#Cargo archivos ······
espectro_hispanos = "/home/eliana/phits/Simulaciones/Quenching_Sevilla/n_HISPANOS.inp"
ene_hispanos, intensidad_hispanos_ua = leer_archivo_de_2_columnnas(espectro_hispanos) #[ene_hispanos] = MeV
#Paso a eV
ene_hispanos_eV = [x *1.0e6 for x in ene_hispanos]

try:
	with open('/home/eliana/Documentos/Neutrones/ENDF/pendf_Si_n_el.json.txt') as file:
		data = json.load(file)
		#print(data)

except json.JSONDecodeError:
	print('Error: Falla al decodificar JSON desde el archivo')

#print(type(data))
print(data.keys())
#print(type(data['datasets']))
#print(len(data['datasets']))
#print(type(data['datasets'][0]))
#print(data['datasets'][0].keys())
#print(type(data['datasets'][0]['pts']))
#print(type(data['datasets'][0]['pts'][0]))
#print(data['datasets'][0]['pts'][0])
#print(data['datasets'][0]['pts'][0]['E'])

#print(a[0])
a=list(data['datasets'][0]['pts'][0].keys())#convierto en una lista el objeto "claves del diccionario que contiene mis datos" 
n_Si_el_dicc = {a[0]:[],a[1]:[],a[2]:[]}

for i, elem in enumerate(data['datasets'][0]['pts']):
	n_Si_el_dicc[a[0]].append(elem[a[0]])
	n_Si_el_dicc[a[1]].append(elem[a[1]])
	n_Si_el_dicc[a[2]].append(elem[a[2]])
	#print(elem)

#print(n_Si_el_dicc['E'])
# Datos del experimento ···················································
# Blanco
volumen = 9.225*2.352*0.0675 #Detector de Si area transversal x espesor [cm]
densidad_Si = 2.33 #[g/cm3]
Mr_Si = 28.085#[u]
NA = 6.023e23#Nº de Avogadro
densidad_atomos_Si=densidad_Si*NA/Mr_Si#átomos de blanco por unidad de volumen
# Fuente de neutrones
flujo_dato = 1e4 #[n/s/cm2]
integ_intensidad_hispanos_ua = sum(intensidad_hispanos_ua)*0.01
#Renormalizo el espectro del paper al flujo de HISPANOS ···
intensidad_hispanos_renorm = [x * flujo_dato/integ_intensidad_hispanos_ua for x in intensidad_hispanos_ua]
print("Integral en unidades arbitrarias del espectro del paper de HISPANOS = ", integ_intensidad_hispanos_ua)

#Calculo Nº de interacciones ··················
# Muy grosso modo ··········
#print(n_Si_el_dicc['E'][66])
#print(n_Si_el_dicc['E'][66])

#Obtengo las posiciones de la lista de energías de ENDF cuyos valores coinciden con las del espectro n_HISPANOS
indice_E_list = []
print("ene_hispanos_eV = ", ene_hispanos_eV)
#b = next(((i, ene) for i, ene in enumerate(n_Si_el_dicc['E']) if ene > 1e4), None)
#print(b)
for y in ene_hispanos_eV:
	#print(y)
	indice_E_list.append(next((i for i, ene in enumerate(n_Si_el_dicc['E']) if ene > y), None))

print('indice_E_list = ', indice_E_list)

# ESTO hay que reemplazarlo por una interpolación o un valor medio ····
sigmas = [n_Si_el_dicc[a[1]][i] for i in indice_E_list]
#·······························································

print("sigmas = ", sigmas)

interacciones = sum([x*y for x, y in zip(sigmas, intensidad_hispanos_renorm)])*1e4*volumen*densidad_atomos_Si

print(interacciones)
#Graficos ······································
plt.plot(n_Si_el_dicc['E'][66:500], n_Si_el_dicc['Sig'][66:500])
plt.yscale('log')
plt.xscale('log')
plt.xlabel('E [eV]')
plt.ylabel('$\sigma_{elastico}$ [barn]')
ax = plt.gca()
ax2 = ax.twinx()
ax2.tick_params(axis='y', labelcolor='r')
ax2.scatter(ene_hispanos_eV, intensidad_hispanos_renorm, color = 'r')

plt.show()

