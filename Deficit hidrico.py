import numpy as np
import pandas as pd
import openpyxl
import xlrd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

def ordenar_datos(ruta_HEC_RAS,Estaciones):
    salida = pd.read_excel(ruta_HEC_RAS, header=2)
    # Se redondea la columna estación para facilitar el filtro
    salida['STATION'] = round(salida['STATION'])
    # Se crea una lista que contenga las estaciones a utilizar
    Estaciones = Estaciones
    # Se extrae el índice de las estaciones con base en el archivo original
    nrows = []
    for i in range(0, len(Estaciones)):
        a = salida.loc[(salida['STATION'] == Estaciones[i])].index[0] + 3
        nrows.append(a)  # Se crea una lista que contenga la fila en la cual se encuentra cada estacion
    # Se utiliza la librería Xlrd para iterar por cada una de las hojas
    datos = xlrd.open_workbook(ruta_HEC_RAS)  # Se abre el archivo nuevamente con la nueva libreria

    # Se itera buscando la información de cada una de las secciones para todos los días
    datos_salida = []
    for dia in range(0, len(datos.sheet_names())):
        c = []  # Lista vacia que se limpia cada vez que se calcule un día
        for i in range(0, len(Estaciones)):
            a = datos.sheet_by_index(dia).cell(nrows[i],2).value  # Con la lista de filas halladas previamente, se busca la celda especificamente
            c.append(a)
        datos_salida.append(c)

    # Se itera buscando la fecha presente en cada hoja
    fecha = []
    for dia in range(0, len(datos.sheet_names())):
        a = datos.sheet_by_index(dia).cell(0, 2).value  # la celda 0,2 es donde se encuentra la fecha en las hojas
        a = a[0:2] + '/' + a[2:5] + '/' + a[5:9]  # Se extrae la cadena de caracteres de la fecha ddmmmyyyy -02apr2010
        datetime_ = str(a)  # Se convierte a cadena
        n = datetime.strptime(datetime_, '%d/%b/%Y')  # Se pasa a un formato fecha que sea aceptado por Python
        fecha.append(n)

    Salidas = pd.DataFrame(datos_salida)  # Se crea un dataframe que contenga los caudales
    Salidas.columns = Estaciones  # Se renombran las columnas con el nombre de las estaciones
    Salidas['Fecha'] = fecha  # Se agrega una nueva columna que contenga las fechas previamente extraidas
    Salidas = Salidas.sort_values(by='Fecha')  # Se ordenan las fechas
    Salidas.set_index('Fecha', inplace=True)  # Se deja como indice el vector de fechas
    Salidas_array=np.array(Salidas).T #Se deja en formato de vectores donde cada vector es un estacion con n dias

    return Salidas_array
#Función para extraer el calado de cada sección, en función de su cota menor
def calado(niveles,cota_menor):
    b=[]
    for i in range(0,len(niveles)):
        a=niveles[i]-cota_menor
        b.append(a)
    return b
#Función para calcular potencial de déficit hídrico de cada sección
def deficit_hidrico(niveles,nivel_critico):
    b=[]
    for i in range(0,len(niveles)):
        a=((niveles[i]-nivel_critico)/nivel_critico)*100
        b.append(a)
    return b
def convertir_dataframe(potencial,fecha,estacion):
    a=pd.DataFrame(potencial,columns=[estacion])
    a['Fecha']=fecha
    a.set_index('Fecha',inplace=True)
    return a

fec1_="01/01/2018"
fec2_="12/31/2018" #Modificar fecha según periodo simulado
fecha=np.array(pd.date_range(fec1_,fec2_))

###Ejemplo río Chicamocha
ruta_HEC_RAS_nivel=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Niveles_ras_RC.xls' #Archivo de niveles (salida HEC-RAS)
nivel_critico_Gensa=1.21 #Nivel crítico definido
nivel_critico_Siberia=0.83 #Nivel crítico definido
nivel_critico_Unidad_Holanda=1.009 #Nivel crítico definido
nivel_critico_QH=0.319 #Nivel crítico definido

#Estaciones Río Chicamocha
Estaciones=[10950, 10500, 10350, 9600, 9300,7050,6750, 6600, 6450, 6300,4350 ,4050, 3750, 2850, 150] #Estaciones dentro del río (Río Chicamocha)
cotas_menores=[2492.4,2489.55,2487.8,2487.8,2487.4,2485.2,2484.8,2485.2,2485.4,2485.2,2484.6,2484,2483.6,2484.31,2482.6] #Cotas menores río Chicamocha
Estaciones=[Estaciones[14]]
cotas_menores=cotas_menores[14]

#Estaciones Quebrada Honda
# Estaciones=[150]
# cotas_menores=2516.25

Niveles=ordenar_datos(ruta_HEC_RAS_nivel,Estaciones) #Se extraen los niveles y se ordenan

calado_est=calado(list(Niveles[0]),cotas_menores)
pdh=deficit_hidrico(calado_est,nivel_critico_Unidad_Holanda)

#Ruta Río Chicamocha
ruta_guardado=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Resultados\Rio_Chicamocha'
#Ruta Quebrada Honda
# ruta_guardado=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Resultados\Quebrada_Honda'
convertir_dataframe(pdh,fecha,Estaciones[len(Estaciones)-1]).to_excel(ruta_guardado+'\\'+'pot_pwd_Unidad_Holanda.xlsx')
