import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def grafica_Quebrada_Honda_niveles(caudales,niveles,label,nombre_columna=150):

    variable_1=caudales[nombre_columna]
    variable_2=niveles[nombre_columna]
    fecha=caudales.index
    fig = plt.figure(figsize=(15, 6))
    x = fecha
    str1 = 'Flow [m3/s]'
    str2 = 'Water level [m]'
    plt.subplot(2, 1, 1)
    plt.plot(x, variable_1, color='#050DF4',label=str(label))
    plt.grid(linestyle=':', linewidth='0.5')
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    plt.ylabel(str1,fontweight='bold', fontsize=15, **{'fontname': 'calibri'})
    plt.xlabel('', fontsize=15, **{'fontname': 'calibri'})
    plt.xlim(fecha[0],fecha[len(fecha)-1])
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(x, variable_2, color='#050DF4',label=str(label))
    plt.grid(linestyle=':', linewidth='0.5')
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    plt.ylabel(str2,fontweight='bold', fontsize=15, **{'fontname': 'calibri'})
    plt.xlabel('', fontsize=15, **{'fontname': 'calibri'})
    plt.xlim(fecha[0], fecha[len(fecha) - 1])
    plt.legend()
    plt.tight_layout()
def graficar_potencial(x, y, niv_inf, niv_med, niv_sup, potencial='deficit hidrico',label='label'):
    """
    potencial=Puede ser deficit hidrico,salinizacion,potencial de renovacion

    """
    plt.figure(figsize=(15, 6))
    colors = ('#CA3701', '#FFAE18', '#FCF7E1', '#2009A9')  # Rojo, Naranja, Pastel, Azul
    if potencial == 'salinizacion':
        colors = colors[::-1]
    else:
        colors = colors
    values = dict(inf=-100000, niv_inf=niv_inf, niv_med=niv_med, niv_sup=niv_sup, sup=100000)
    for i in range(0, len(values)):
        globals()[list(values.keys())[i]] = [values.get((list(values.keys())[i])) for j in range(0, len(fecha))]

    for i in range(0, len(values) - 1):
        plt.fill_between(fecha, globals()[list(values.keys())[i]], globals()[list(values.keys())[i + 1]],
                         color=colors[i])
    plt.scatter(x, y, s=6, c='black', edgecolors='black')
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    plt.ylabel(str(label)+' [%]',fontweight='bold',fontsize=16, **{'fontname': 'calibri'})
    # plt.grid(linestyle=':', linewidth='0.5')
    plt.ylim(min(y) - 2, max(y) + 2)
    plt.xlim(fecha[0], fecha[len(fecha) - 1])
def clasificarPotencial(MuyAlto, Alto, Moderado, Bajo,
                        Limite1, Limite2, Limite3, Serie):
    longitudSerie = len(Serie)

    for posicion in range(longitudSerie):
        if Serie[posicion] <= Limite1:
            MuyAlto.append(posicion)
        elif Serie[posicion] > Limite1 and Serie[posicion] <= Limite2:
            Alto.append(posicion)
        elif Serie[posicion] > Limite2 and Serie[posicion] <= Limite3:
            Moderado.append(posicion)
        elif Serie[posicion] > Limite3:
            Bajo.append(posicion)
def clasificarPotencialSalinizacion(MuyAlto, Alto, Moderado, Bajo,
                                    Limite1, Limite2, Limite3, Serie):
    longitudSerie = len(Serie)

    for posicion in range(longitudSerie):
        if Serie[posicion] >= Limite1:
            MuyAlto.append(posicion)
        elif Serie[posicion] >= Limite1 and Serie[posicion] < Limite2:
            Alto.append(posicion)
        elif Serie[posicion] >= Limite2 and Serie[posicion] < Limite3:
            Moderado.append(posicion)
        elif Serie[posicion] < Limite3:
            Bajo.append(posicion)
def hallarPorcentajeCategoria(MuyAlto, Alto, Moderado, Bajo, longitudSerie):
    listaPorcentajes = []
    PorcentajeMuyAlto = (100 * len(MuyAlto)) / longitudSerie
    listaPorcentajes.append(PorcentajeMuyAlto)
    PorcentajeAlto = (100 * len(Alto)) / longitudSerie
    listaPorcentajes.append(PorcentajeAlto)
    PorcentajeModerado = (100 * len(Moderado)) / longitudSerie
    listaPorcentajes.append(PorcentajeModerado)
    PorcentajeBajo = (100 * len(Bajo)) / longitudSerie
    listaPorcentajes.append(PorcentajeBajo)

    return (listaPorcentajes)
def hallarConceptoGlobal(PorcentajeMuyAlto, PorcentajeAlto, PorcentajeModerado, PorcentajeBajo):
    var = {PorcentajeMuyAlto: "Muy Alto", PorcentajeAlto: "Alto", PorcentajeModerado: "Moderado",
           PorcentajeBajo: "Bajo"}
    if ((PorcentajeMuyAlto >= 25 and PorcentajeMuyAlto <= 100) & (PorcentajeAlto >= 0 and PorcentajeAlto <= 50) & (
            PorcentajeModerado >= 0 and PorcentajeModerado < 50) & (PorcentajeBajo >= 0 and PorcentajeBajo < 25)):
        ConceptoGlobal = "Muy Alto"
    elif ((PorcentajeMuyAlto >= 0 and PorcentajeMuyAlto < 25) & (PorcentajeAlto > 25 and PorcentajeAlto <= 100) & (
            PorcentajeModerado >= 0 and PorcentajeModerado <= 50) & (PorcentajeBajo >= 0 and PorcentajeBajo < 25)):
        ConceptoGlobal = "Alto"
    elif ((PorcentajeMuyAlto >= 0 and PorcentajeMuyAlto <= 25) & (PorcentajeAlto >= 0 and PorcentajeAlto <= 50) & (
            PorcentajeModerado >= 25 and PorcentajeModerado <= 100) & (PorcentajeBajo >= 0 and PorcentajeBajo <= 75)):
        ConceptoGlobal = "Moderado"
    elif ((PorcentajeMuyAlto >= 0 and PorcentajeMuyAlto < 25) & (PorcentajeAlto >= 0 and PorcentajeAlto < 25) & (
            PorcentajeModerado >= 0 and PorcentajeModerado < 25) & (PorcentajeBajo > 75 and PorcentajeBajo <= 100)):
        ConceptoGlobal = "Bajo"
    else:
        ConceptoGlobal = max(var)
    return (ConceptoGlobal)
def generarDatosOSI(OPR, OPs, OPd):
    OSI = []
    longitudOSI = len(OPR)
    for i in range(longitudOSI):
        if (OPR[i] == 1 and OPs[i] == 1 and OPd[i] == 1):
            OSI.insert(i, 1)  # susceptibilidad conjunta muy alta
        elif (OPR[i] >= 2 and OPs[i] <= 2 and OPd[i] <= 2):
            OSI.insert(i, 2)  # susceptibilidad conjunta alta
        elif (OPR[i] <= 2 and OPs[i] >= 2 and OPd[i] <= 2):
            OSI.insert(i, 2)  # susceptibilidad conjunta alta
        elif (OPR[i] <= 2 and OPs[i] <= 2 and OPd[i] >= 2):
            OSI.insert(i, 2)  # susceptibilidad conjunta alta
        elif (OPR[i] >= 3 and OPs[i] >= 3 and OPd[i] <= 3):
            OSI.insert(i, 3)  # susceptibilidad conjunta moderada
        elif (OPR[i] >= 3 and OPs[i] <= 3 and OPd[i] >= 3):
            OSI.insert(i, 3)  # susceptibilidad conjunta moderada
        elif (OPR[i] <= 3 and OPs[i] >= 3 and OPd[i] >= 3):
            OSI.insert(i, 3)  # susceptibilidad conjunta moderada
        elif (OPR[i] == 4 and OPs[i] == 4 and OPd[i] == 4):
            OSI.insert(i, 4)  # susceptibilidad conjunta baja
        else:
            OSI.insert(i, 0)
    return (OSI)
def insertarDatosPotencialOSI(MuyAltoPotencial, AltoPotencial, ModeradoPotencial, BajoPotencial, OSIPotencial):
    for i in range(len(MuyAltoPotencial)):
        OSIPotencial.insert(MuyAltoPotencial[i], 1)
    for i in range(len(AltoPotencial)):
        OSIPotencial.insert(AltoPotencial[i], 2)
    for i in range(len(ModeradoPotencial)):
        OSIPotencial.insert(ModeradoPotencial[i], 3)
    for i in range(len(BajoPotencial)):
        OSIPotencial.insert(BajoPotencial[i], 4)
def grafica_OSI(fecha, serieOSI):
    OSIMA = []
    OSIA = []
    OSIM = []
    OSIB = []
    for i in range(len(serieOSI)):
        OSIMA.append(1)
        OSIA.append(2)
        OSIM.append(3)
        OSIB.append(4)
    plt.figure(figsize=(15, 6))
    plt.plot(fecha, OSIB, color='b', label='Low')
    plt.plot(fecha, OSIM, color='y', label='Moderate')
    plt.plot(fecha, OSIA, color='#FF8000', label='High')
    plt.plot(fecha, OSIMA, color='r', label='Very High')
    plt.plot(fecha, serieOSI, 'ok', label='OSI')
    # Coloco la leyenda y la ubico con un tamaño específico
    plt.legend(loc='upper right', bbox_to_anchor=(1.12, 0.65), fontsize=10, shadow=True, borderpad=0.2)
    plt.grid(linestyle=':', linewidth='0.5')
    plt.xlim(fecha[0], fecha[len(fecha) - 1])

    plt.ylabel('Overall susceptibility index (OSI)',fontweight='bold',fontsize=14, **{'fontname': 'calibri'})
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    # plt.savefig(ruta_imagenes+'\\'+str(año)+'_'+str(esc)+'.png')
def calculo_OSI(pot_def_hid,pot_sal,pot_rev,LimitePWd1,LimitePWd2,LimitePWd3,
                LimitePR1,LimitePR2,LimitePR3,
                LimitePS1,LimitePS2,LimitePS3):
    #Calculo de potenciales
    #Potencial de déficit hídrico
    # Establezco Serie y límites
    SeriePwd = pot_def_hid
    longitudSerie = len(SeriePwd)
    # Definición de categorias
    MuyAltoPWd,AltoPWd,ModeradoPWd,BajoPWd = [],[],[],[]
    # Invoco función clasificarPotencial
    clasificarPotencial(MuyAltoPWd, AltoPWd, ModeradoPWd, BajoPWd, LimitePWd1, LimitePWd2, LimitePWd3, SeriePwd)
    # Invoco función hallar porcentaje por categoría
    porcentajes = hallarPorcentajeCategoria(MuyAltoPWd, AltoPWd, ModeradoPWd, BajoPWd, longitudSerie)
    # Asigno cada porcentaje
    PorcentajeMuyAltoPWd,PorcentajeAltoPWd,PorcentajeModeradoPWd,PorcentajeBajoPWd = porcentajes[0],porcentajes[1],\
                                                                                     porcentajes[2],porcentajes[3]
    # InvocoFunción para hallar concepto Global
    conceptoGlobalPWd = hallarConceptoGlobal(PorcentajeMuyAltoPWd, PorcentajeAltoPWd, PorcentajeModeradoPWd,
                                             PorcentajeBajoPWd)
    #Potencial de renovación
    # Establezco Serie y límites
    SeriePR = pot_rev
    longitudSerie = len(SeriePR)
    # Definición de categorias
    MuyAltoPR,AltoPR,ModeradoPR,BajoPR = [],[],[],[]
    # Invoco función clasificarPotencial
    clasificarPotencial(MuyAltoPR, AltoPR, ModeradoPR, BajoPR, LimitePR1, LimitePR2, LimitePR3, SeriePR)
    # Invoco función hallar porcentaje por categoría
    porcentajes = hallarPorcentajeCategoria(MuyAltoPR, AltoPR, ModeradoPR, BajoPR, longitudSerie)
    # Asigno cada porcentaje
    PorcentajeMuyAltoPR,PorcentajeAltoPR,PorcentajeModeradoPR,PorcentajeBajoPR = porcentajes[0],porcentajes[1],\
                                                                                 porcentajes[2],porcentajes[3]
    # InvocoFunción para hallar concepto Global
    conceptoGlobalPR = hallarConceptoGlobal(PorcentajeMuyAltoPR, PorcentajeAltoPR, PorcentajeModeradoPR, PorcentajeBajoPR)
    #Potencial de salinización
    SeriePS = pot_sal
    longitudSerie = len(SeriePS)
    # Definición de categorias
    MuyAltoPS,AltoPS,ModeradoPS,BajoPS = [],[],[],[]
    # Invoco función clasificarPotencial
    clasificarPotencialSalinizacion(MuyAltoPS, AltoPS, ModeradoPS, BajoPS, LimitePS1, LimitePS2, LimitePS3, SeriePS)
    # Invoco función hallar porcentaje por categoría
    porcentajes = hallarPorcentajeCategoria(MuyAltoPS, AltoPS, ModeradoPS, BajoPS, longitudSerie)
    # Asigno cada porcentaje
    PorcentajeMuyAltoPS,PorcentajeAltoPS,PorcentajeModeradoPS,PorcentajeBajoPS = porcentajes[0],porcentajes[1],\
                                                                                 porcentajes[2],porcentajes[3]
    # InvocoFunción para hallar concepto Global
    conceptoGlobalPS = hallarConceptoGlobal(PorcentajeMuyAltoPS, PorcentajeAltoPS,
                                            PorcentajeModeradoPS, PorcentajeBajoPS)
    #Cálculo de OSI
    OPR,OPs,OPd,OSI=[],[],[],[]
    #PotencialRenovación
    insertarDatosPotencialOSI(MuyAltoPR, AltoPR, ModeradoPR, BajoPR, OPR)
    #PotencialSalinizacion
    insertarDatosPotencialOSI(MuyAltoPS, AltoPS, ModeradoPS, BajoPS, OPs)
    #Potencial Déficit
    insertarDatosPotencialOSI(MuyAltoPWd, AltoPWd, ModeradoPWd, BajoPWd, OPd)
    #Invoco generarOSI
    serieOSI=generarDatosOSI(OPR, OPs, OPd)
    #print(serieOSI)
    #----Algoritmo OSI
    longitudSerie=len(serieOSI)
    #Definición de categorias
    MuyAltoOSI,AltoOSI,ModeradoOSI,BajoOSI=[],[],[],[]
    #Invoco función clasificarPotencial
    clasificarPotencial(MuyAltoOSI, AltoOSI, ModeradoOSI, BajoOSI, 1, 2, 3, serieOSI)
    #Invoco función hallar porcentaje por categoría
    porcentajes = hallarPorcentajeCategoria(MuyAltoOSI, AltoOSI, ModeradoOSI, BajoOSI, longitudSerie)
    #Asigno cada porcentaje
    PorcentajeMuyAltoOSI,PorcentajeAltoOSI,PorcentajeModeradoOSI,PorcentajeBajoOSI=porcentajes[0],porcentajes[1],\
                                                                                   porcentajes[2],porcentajes[3]
    #InvocoFunción para hallar concepto Global
    conceptoGlobalOSI=hallarConceptoGlobal(PorcentajeMuyAltoOSI, PorcentajeAltoOSI, PorcentajeModeradoOSI, PorcentajeBajoOSI)

    return serieOSI,conceptoGlobalOSI,PorcentajeMuyAltoOSI,PorcentajeAltoOSI,PorcentajeModeradoOSI,PorcentajeBajoOSI

#Se definen las fechas de simulación
fec1="01/01/2018"
fec2="12/31/2018" #Modificar fecha según periodo simulado
fecha=np.array(pd.date_range(fec1,fec2))

#-------------------------------------------- QUEBRADA HONDA---------------------------------------------------------#

#Se grafica nivel y caudal en la estación 150 de Quebrada Honda
ruta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Resultados\Quebrada_Honda'
caudales=pd.read_excel(ruta+'\\'+'Caudales.xlsx',header=0,index_col='Fecha')
niveles=pd.read_excel(ruta+'\\'+'Nivel.xlsx',header=0,index_col='Fecha')
label='Quebrada Honda'
grafica_Quebrada_Honda_niveles(caudales,niveles,label)
plt.savefig(ruta+'\\'+'Caudales.png')
plt.show()
#Se grafican los potenciales para Quebrada Honda
pot_rev=pd.read_excel(ruta+'\\'+'pot_rev.xlsx',header=0,index_col='Fecha')
pot_pwd=pd.read_excel(ruta+'\\'+'pot_pwd.xlsx',header=0,index_col='Fecha')
pot_sal=pd.read_excel(ruta+'\\'+'pot_sal.xlsx',header=0,index_col='Fecha')
pot_rev,pot_sal,pot_pwd=list(pot_rev[pot_rev.columns[0]]),list(pot_sal[pot_sal.columns[0]]),list(pot_pwd[pot_pwd.columns[0]])
graficar_potencial(fecha,pot_rev,93.54,94.36,94.43,
                   potencial='renovación',label='Renewal potential')
plt.savefig(ruta+'\\'+'potencial_de_renovacion.png')
plt.show()
graficar_potencial(fecha, pot_sal, 955.49 ,1073, 4279,
                  potencial='salinizacion',label='Salinization potential')
plt.savefig(ruta+'\\'+'potencial_de_salinizacion.png')
plt.show()
graficar_potencial(fecha, pot_pwd, -44.44, -1.15, 121.22,
                   potencial='deficit hidrico',label='Water deficit potential')
plt.savefig(ruta+'\\'+'potencial_de_deficit_hidrico.png')
plt.show()
serieOSI,conceptoGlobalOSI=calculo_OSI(pot_pwd,pot_sal,pot_rev,-44.44, -1.15, 121.22,
                                       93.54,94.36,94.43,955.49 ,1073, 4279)
print('Quebrada Honda ',conceptoGlobalOSI)
grafica_OSI(fecha,serieOSI)
plt.savefig(ruta+'\\'+'OSI.png')
plt.show()
#-------------------------------------------- RÍO CHICAMOCHA---------------------------------------------------------#
#Se grafica nivel y caudal en la estación 7050 del Río Chicamocha
ruta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Resultados\Rio_Chicamocha'
caudales=pd.read_excel(ruta+'\\'+'Caudales.xlsx',header=0,index_col='Fecha')
niveles=pd.read_excel(ruta+'\\'+'Nivel.xlsx',header=0,index_col='Fecha')
label='Rio Chicamocha-Sector Gensa'
grafica_Quebrada_Honda_niveles(caudales,niveles,label,nombre_columna=7050)
plt.savefig(ruta+'\\'+'Caudales_Gensa.png')
plt.show()
#Se grafican los potenciales para Río Chicamocha Gensa
pot_rev=pd.read_excel(ruta+'\\'+'pot_rev_Gensa.xlsx',header=0,index_col='Fecha')
pot_pwd=pd.read_excel(ruta+'\\'+'pot_pwd_Gensa.xlsx',header=0,index_col='Fecha')
pot_sal=pd.read_excel(ruta+'\\'+'pot_sal_Gensa.xlsx',header=0,index_col='Fecha')

pot_rev,pot_sal,pot_pwd=list(pot_rev[7050]),list(pot_sal[7050]),list(pot_pwd[7050])
graficar_potencial(fecha,pot_rev,66.06,66.13,66.15,
                   potencial='renovación',label='Renewal potential')
plt.savefig(ruta+'\\'+'potencial_de_renovacion_Gensa.png')
plt.show()
graficar_potencial(fecha, pot_sal,591.67 ,668,2336,
                  potencial='salinizacion',label='Salinization potential')
plt.savefig(ruta+'\\'+'potencial_de_salinizacion_Gensa.png')
plt.show()
graficar_potencial(fecha, pot_pwd, -9.34, 14.89, 43.36,
                   potencial='deficit hidrico',label='Water deficit potential')
plt.savefig(ruta+'\\'+'potencial_de_deficit_hidrico_Gensa.png')
plt.show()
serieOSI,conceptoGlobalOSI=calculo_OSI(pot_pwd,pot_sal,pot_rev,
                                       9.34, 14.89, 43.36,
                                       66.06,66.13,66.15,
                                       591.67 ,668,2336)
print('Gensa ',conceptoGlobalOSI)
grafica_OSI(fecha,serieOSI)
plt.savefig(ruta+'\\'+'OSI_Gensa.png')
plt.show()
############################
#Se grafica nivel y caudal en la estación 4350 del Río Chicamocha
caudales=pd.read_excel(ruta+'\\'+'Caudales.xlsx',header=0,index_col='Fecha')
niveles=pd.read_excel(ruta+'\\'+'Nivel.xlsx',header=0,index_col='Fecha')
label='Rio Chicamocha-Sector Siberia'
grafica_Quebrada_Honda_niveles(caudales,niveles,label,nombre_columna=4350)
plt.savefig(ruta+'\\'+'Caudales_Siberia.png')
plt.show()
#Se grafican los potenciales para Río Chicamocha Gensa
pot_rev=pd.read_excel(ruta+'\\'+'pot_rev_Siberia.xlsx',header=0,index_col='Fecha')
pot_pwd=pd.read_excel(ruta+'\\'+'pot_pwd_Siberia.xlsx',header=0,index_col='Fecha')
pot_sal=pd.read_excel(ruta+'\\'+'pot_sal_Siberia.xlsx',header=0,index_col='Fecha')

pot_rev,pot_sal,pot_pwd=list(pot_rev[4350]),list(pot_sal[4350]),list(pot_pwd[4350])
graficar_potencial(fecha,pot_rev,59.18,59.22,59.4,
                   potencial='renovación',label='Renewal potential')
plt.savefig(ruta+'\\'+'potencial_de_renovacion_Siberia.png')
plt.show()
graficar_potencial(fecha, pot_sal,310.8,356,1347,
                  potencial='salinizacion',label='Salinization potential')
plt.savefig(ruta+'\\'+'potencial_de_salinizacion_Siberia.png')
plt.show()
graficar_potencial(fecha, pot_pwd, -59.92,21.05,79.73,
                   potencial='deficit hidrico',label='Water deficit potential')
plt.savefig(ruta+'\\'+'potencial_de_deficit_hidrico_Siberia.png')
plt.show()
serieOSI,conceptoGlobalOSI=calculo_OSI(pot_pwd,pot_sal,pot_rev,
                                       -59.92,21.05,79.73,
                                       59.18,59.22,59.4,
                                       9310.8,356,1347)
print('Siberia ',conceptoGlobalOSI)
grafica_OSI(fecha,serieOSI)
plt.savefig(ruta+'\\'+'OSI_Siberia.png')
plt.show()
##############################
#Se grafica nivel y caudal en la estación 150 del Río Chicamocha
caudales=pd.read_excel(ruta+'\\'+'Caudales.xlsx',header=0,index_col='Fecha')
niveles=pd.read_excel(ruta+'\\'+'Nivel.xlsx',header=0,index_col='Fecha')
label='Rio Chicamocha-Sector Unidad Holanda'
grafica_Quebrada_Honda_niveles(caudales,niveles,label,nombre_columna=150)
plt.savefig(ruta+'\\'+'potencial_de_renovacion_Unidad_Holanda.png')
plt.savefig(ruta+'\\'+'Caudales_Unidad_Holanda.png')
plt.show()
#Se grafican los potenciales para Río Chicamocha Unidad_Holanda
pot_rev=pd.read_excel(ruta+'\\'+'pot_rev_Unidad_Holanda.xlsx',header=0,index_col='Fecha')
pot_pwd=pd.read_excel(ruta+'\\'+'pot_pwd_Unidad_Holanda.xlsx',header=0,index_col='Fecha')
pot_sal=pd.read_excel(ruta+'\\'+'pot_sal_Unidad_Holanda.xlsx',header=0,index_col='Fecha')

pot_rev,pot_sal,pot_pwd=list(pot_rev[150]),list(pot_sal[150]),list(pot_pwd[150])
graficar_potencial(fecha,pot_rev,59.19,59.23,59.31,
                   potencial='renovación',label='Renewal potential')
plt.savefig(ruta+'\\'+'potencial_de_renovacion_Unidad_Holanda.png')
plt.show()
graficar_potencial(fecha, pot_sal,95.92,118,590,
                  potencial='salinizacion',label='Salinization potential')
plt.savefig(ruta+'\\'+'potencial_de_salinizacion_Unidad_Holanda.png')
plt.show()
graficar_potencial(fecha, pot_pwd, -39.87,18.88,43.2,
                   potencial='deficit hidrico',label='Water deficit potential')
plt.savefig(ruta+'\\'+'potencial_de_deficit_hidrico_Unidad_Holanda.png')
plt.show()
serieOSI,conceptoGlobalOSI=calculo_OSI(pot_pwd,pot_sal,pot_rev,
                                       -39.87,18.88,43.2,
                                       59.19, 59.23, 59.31,
                                       95.92,118,590)
print('Unidad_Holanda ',conceptoGlobalOSI)
grafica_OSI(fecha,serieOSI)
plt.savefig(ruta+'\\'+'OSI_Unidad_Holanda.png')
plt.show()

