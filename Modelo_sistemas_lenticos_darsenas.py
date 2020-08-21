import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates

# Definición de la expresión para el cálculo de la salinidad en unidades de Kg/m3 a
# partir de la conductividad a 25ºc
def salinidad(conductividad, temperatura):
    C_KCL = 4.2914  # conductividad de la solución de referencia a 15ºC (S/m) Unesco,1981
    Tc = 15  # Temperatura de la solución standard ºC
    C_KCL25 = (C_KCL * 10000) / (1 + (0.0191 * (
                Tc - 25)))  # se expresa la conductividad de la solución de referencia a 25ºC, empleando una aproximación asumiendo que no existe una temperatura interna de compensación en la celda de medición
    # 10000 para hacer la conversión de S/m a microohms/cm
    a0 = 0.0080
    a1 = -0.1692
    a2 = 25.3851
    a3 = 14.0941
    a4 = -7.0261
    a5 = 2.7081
    b0 = 0.0005
    b1 = -0.0056
    b2 = -0.0066
    b3 = -0.0375
    b4 = 0.0636
    b5 = -0.0144
    # Cálculo de la conductividad a 25ºC
    XT = temperatura - 15
    RT35 = (((1.0031E-9 * XT - 6.9698E-7) * XT + 1.104259E-4) * XT + 2.00564E-2) * XT + 0.6766097

    if (temperatura == 25).any():  # El .any() permite emplear series temporales
        C_25 = conductividad * 1000  # corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    else:
        C_25 = 1000 * conductividad / (1 + 0.0191 * (
                    temperatura - 25))  # corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    # Relación de conductividades ajustes por efecto de temperatura y cálculo de
    # la salinidad
    # Para salinidades entre 0 y 40 ups
    Rt = C_25 / C_KCL25
    X = 400 * Rt
    Y = 100 * Rt
    f = XT / (1 + 0.0162 * XT)
    deltaS = (f) * (b0 + b1 * Rt ** (1 / 2) + b2 * Rt + b3 * Rt ** (3 / 2) + b4 * Rt ** 2 + b5 * Rt ** (5 / 2))
    S = a0 + a1 * Rt ** (1 / 2) + a2 * Rt + a3 * Rt ** (3 / 2) + a4 * Rt ** 2 + a5 * Rt ** (5 / 2) + deltaS
    salinidad = S - (a0 / (1 + 1.5 * X + X ** 2)) - b0 * f / (1 + Y ** (1 / 2) + Y ** (3 / 2))

    return salinidad  # Salinidad en kg/m3
# Definición de la expresión para el cálculo de la salinidad en unidades de Kg/m3 a
# partir de la conductividad a 25ºc
def salinidad1(conductividad, temperatura):
    C_KCL = 4.2914  # conductividad de la solución de referencia a 15ºC (S/m) Unesco,1981
    Tc = 15  # Temperatura de la solución standard ºC
    C_KCL25 = (C_KCL * 10000) / (1 + (0.0191 * (
                Tc - 25)))  # se expresa la conductividad de la solución de referencia a 25ºC, empleando una aproximación asumiendo que no existe una temperatura interna de compensación en la celda de medición
    # 10000 para hacer la conversión de S/m a microohms/cm
    a0 = 0.0080
    a1 = -0.1692
    a2 = 25.3851
    a3 = 14.0941
    a4 = -7.0261
    a5 = 2.7081
    b0 = 0.0005
    b1 = -0.0056
    b2 = -0.0066
    b3 = -0.0375
    b4 = 0.0636
    b5 = -0.0144
    # Cálculo de la conductividad a 25ºC
    XT = temperatura - 15
    RT35 = (((1.0031E-9 * XT - 6.9698E-7) * XT + 1.104259E-4) * XT + 2.00564E-2) * XT + 0.6766097

    if temperatura == 25:  # El .any() permite emplear series temporales
        C_25 = conductividad * 1000  # corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    else:
        C_25 = 1000 * conductividad / (1 + 0.0191 * (
                    temperatura - 25))  # corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    # Relación de conductividades ajustes por efecto de temperatura y cálculo de
    # la salinidad
    # Para salinidades entre 0 y 40 ups
    Rt = C_25 / C_KCL25
    X = 400 * Rt
    Y = 100 * Rt
    f = XT / (1 + 0.0162 * XT)
    deltaS = (f) * (b0 + b1 * Rt ** (1 / 2) + b2 * Rt + b3 * Rt ** (3 / 2) + b4 * Rt ** 2 + b5 * Rt ** (5 / 2))
    S = a0 + a1 * Rt ** (1 / 2) + a2 * Rt + a3 * Rt ** (3 / 2) + a4 * Rt ** 2 + a5 * Rt ** (5 / 2) + deltaS
    salinidad = S - (a0 / (1 + 1.5 * X + X ** 2)) - b0 * f / (1 + Y ** (1 / 2) + Y ** (3 / 2))

    return salinidad  # Salinidad en kg/m3
def Ab1(x, a=1.391e+06, b=4192, c=6.023):
    # x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
    # Ley de áreas para el Lago (área en m^2) , ajuste mediante función
    # logística

    # Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if (x <= 0):
        Ab = 0  # (en m^2)
    else:
        Ab = (a * b * 2.718281 ** (c * x)) / (a + b * (2.718281 ** (6.008 * x)) - 1)  # (en m^2)

    return Ab
def Area_dar1(x, a=271.88902077, b=-1925.40179148, c=5346.75787005,d=-7508.69710111,e=6639.38465588,f=-93.74337132):
    # x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
    # Ley de áreas para el Lago (área en m^2) , ajuste mediante función
    # logística

    # Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if (x <= 0.0144):
        Ab = 0  # (en m^2)
    else:
        Ab = (a*(x**5))+(b*(x**4))+(c*(x**3))+(d*(x**2))+(e*(x))+f # (en m^2)
    return Ab
def Area_dar2(x, a=-1482.24872765, b=18167.68264678, c=-64707.50734129,d=97886.66908086,e=-19430.68615198 ,f=464.18587539):
    # x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
    # Ley de áreas para el Lago (área en m^2) , ajuste mediante función
    # logística

    # Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if x<=0 and x<0.2:
        Ab = 0  # (en m^2)
    else:
        Ab = (a*(x**5))+(b*(x**4))+(c*(x**3))+(d*(x**2))+(e*(x))+f # (en m^2)
    return Ab
def compuerta(a, b, y2, cc=0.42, c1=0.0979):
    if a == 0:
        Qe1 = 0
    else:
        if y2 / a >= 2.451:
            cv = 1
        else:
            if a == 0:
                cv = 0.96
                v1 = 0
            else:
                cv = 0.96 + (c1 * a / y2)

        v1 = cv * ((2 * 9.81 * y2) ** 0.5) / ((1 + (cc * a / y2)) ** 0.5)
        cd = (cc * cv) / ((1 + (cc * a / y2)) ** 0.5)
        Qe1 = cd * ((2 * 9.81 * y2) ** 0.5) * a * b

    return (Qe1)
def Bombeo_darsena_1(hor_bom, potencia=234):
    caudal = hor_bom * potencia / 86400
    return caudal
# Generación de los niveles en función de los caudales afluentes
def Dinamica_darsena_1(No, prec, evap, dq_ant, hor_bom):
    """
    Parámetros
    ----------------------------------------------------------------------------------------------------------------------
    No=Nivel inicial del lago
    Cfl=Cota de fondo lago
    Cfc=Cota de fondo compuerta
    aper_com=régimen de apertura de compuerta
    prec=serie temporal de precipitacion [mm]
    evap=serie temporal de evaporacion [mm]
    dq=delta de caudales antrópicos [m3/s]
    q_hid=Serie de caudal hidrológico [m3/s]
    """
    Ao = Area_dar1(No, -747.6, 3195.9, 320.76)  # Se cálcula el área inicial
    Caudal_prec = []
    Caudal_evap = []
    delta_cau = []
    Alturas = []
    Areas_mod = []
    Caudal_salida = []
    for i in range(0, len(fecha)):
        if i == 0:
            Q_p = prec[i] / (86400 * 1000) * Ao  # Se calcula el caudal por precipitación en función del área inicial
            Q_e = evap[i] / (86400 * 1000) * Ao  # Se calcula el caudal por evaporación en función del área inicial
            bomb = Bombeo_darsena_1(hor_bom[i])
            dq = Q_p - Q_e - bomb + dq_ant[i]  # Se realiza el balance de masas
            Alt_m = (dq / Ao * 86400) + No  # Se calcula la áltura de la lámina de agua en función del caudal
            Are_m = Area_dar1(Alt_m)  # Se calcula la nueva área ocupada posterior al balance
        if i > 0:
            Q_p = prec[i] / (86400 * 1000) * Areas_mod[i - 1]
            Q_e = evap[i] / (86400 * 1000) * Areas_mod[i - 1]
            bomb = Bombeo_darsena_1(hor_bom[i])
            dq = Q_p - Q_e - bomb + dq_ant[i]
            Alt_m = (dq / Areas_mod[i - 1] * 86400) + Alturas[i - 1]
            Are_m = Area_dar1(Alt_m)
        print(dq_ant[i])
        Caudal_prec.append(Q_p)  # lista de caudales por precipitación
        Caudal_evap.append(Q_e)  # lista de caudales por evaporación
        delta_cau.append(dq)  # lista de variación diaria de caudales
        Caudal_salida.append(bomb)  # Caudal de salida por la compuerta
        Alturas.append(Alt_m)  # Niveles del lago
        Areas_mod.append(Are_m)  # Area superficial del lago
    Alturas = np.array(Alturas)
    Caudal_salida = np.array(Caudal_salida)
    Areas_mod = np.array(Areas_mod)
    return Alturas, Caudal_salida, Areas_mod
# Generación de los niveles en función de los caudales afluentes
def Dinamica_Darsena2(No, Cfl, Cfc, prec, evap, dq_ant, cau_dar1, aper_com):
    # cambiar 1.12 de la compuerta
    """
    Parámetros
    ----------------------------------------------------------------------------------------------------------------------
    No=Nivel inicial del lago
    Cfl=Cota de fondo lago
    Cfc=Cota de fondo compuerta
    aper_com=régimen de apertura de compuerta
    prec=serie temporal de precipitacion [mm]
    evap=serie temporal de evaporacion [mm]
    dq=delta de caudales antrópicos [m3/s]
    q_hid=Serie de caudal hidrológico [m3/s]
    """
    y = Cfl - Cfc  # Cálcula la diferencia entre la cota inferior del lago y la cota inferior de la compuerta
    No_com = No - y - aper_com[0] * 2 / 100  # Cálcula la lámina de agua sobre la compuerta
    Ao = Area_dar2(No, 11444, 19653, -2692.7)  # Se cálcula el área inicial
    Nivel_com = []
    Caudal_prec = []
    Caudal_evap = []
    delta_cau = []
    Alturas = []
    Areas_mod = []
    Caudal_salida = []
    for i in range(0, len(fecha)):
        if i == 0:
            Q_p = prec[i] / (86400 * 1000) * Ao  # Se calcula el caudal por precipitación en función del área inicial
            Q_e = evap[i] / (86400 * 1000) * Ao  # Se calcula el caudal por evaporación en función del área inicial
            aper = compuerta(aper_com[i] * 0.02, 1.5, No_com)
            dq = Q_p - Q_e - aper + dq_ant[i] + cau_dar1[i]  # Se realiza el balance de masas
            Alt_m = (dq / Ao * 86400) + No  # Se calcula la áltura de la lámina de agua en función del caudal
            Are_m = Area_dar2(Alt_m, 11444, 19653, -2692.7)  # Se calcula la nueva área ocupada posterior al balance
            N_c = Alt_m - y + aper_com[i] * 0.02  # Se calcula la lámina de agua sobre la compuerta
        if i > 0:
            Q_p = prec[i] / (86400 * 1000) * Areas_mod[i - 1]
            Q_e = evap[i] / (86400 * 1000) * Areas_mod[i - 1]
            aper = compuerta(aper_com[i] * 0.02, 1.5, Nivel_com[i - 1])
            dq = Q_p - Q_e - aper + dq_ant[i] + cau_dar1[i]
            Alt_m = (dq / Areas_mod[i - 1] * 86400) + Alturas[i - 1]
            Are_m = Area_dar2(Alt_m, 11444, 19653, -2692.7)
            N_c = Alt_m - y + aper_com[i] * 0.02
        Nivel_com.append(N_c)
        Caudal_prec.append(Q_p)  # lista de caudales por precipitación
        Caudal_evap.append(Q_e)  # lista de caudales por evaporación
        delta_cau.append(dq)  # lista de variación diaria de caudales
        Caudal_salida.append(aper)  # Caudal de salida por la compuerta
        Alturas.append(Alt_m)  # Niveles del lago
        Areas_mod.append(Are_m)  # Area superficial del lago
    Alturas = np.array(Alturas)
    Caudal_salida = np.array(Caudal_salida)
    Areas_mod = np.array(Areas_mod)
    return Alturas, Caudal_salida, Areas_mod
def salinizacion(vol_sis, cargas_afluentes, caudales_efl, con_inicial, tem_inicial, con_geo=2.5,
                              tem_geo=21.2):
    """
    Parámetros
    ----------------------------------------------------------------------------------------------------------------------
    vol_sis=Serie temporal de volumen del sistema
    carga_salinidad=Serie temporal de carga total de salinidad aportante al sistema
    con_inicial=Conductividad inicial del sistema al t=0
    tem_inicial=Temperatura inicial del sistema al t=0
    """
    Sal=[]
    ps=[]
    Ci=salinidad1(con_inicial, tem_inicial)
    Co=Ci
    for i in range(0, 365):

        Mooas3=(Ci * vol_sis[i])+(cargas_afluentes[i])*86400
        Msaas=(caudales_efl[i]*Co)*86400
        Mtaas=Mooas3-Msaas

        if i>0:
            Co=Sal[i-1]
        if i<364:
            a=Mtaas/vol_sis[i+1]
        Sal.append(a)
    sg=salinidad1(con_geo,tem_geo)

    for i in range(0,len(Sal)):
        a=Sal[i]/sg*100
        ps.append(a)
    return Sal  # Serie temporal de potencial de salinidad
def Abrir_excel(ruta_carpeta, nombre_excel, nombre_hoja):
    vars()[str(nombre_hoja)] = pd.read_excel(ruta_carpeta + '\\' + str(nombre_excel) + '.xlsx', header=0,
                                             index_col='Fecha', sheet_name=str(nombre_hoja))
    return vars()[str(nombre_hoja)]
# Caudales antrópicos delta
def caudales_antropicos(Afluentes, Efluentes):
    dq_ant = []
    afl = []
    efl = []
    for i in range(0, Afluentes.shape[0]):
        a = np.sum(Afluentes.iloc[i].values)
        b = np.sum(Efluentes.iloc[i].values)
        delt = a - b
        dq_ant.append(delt)  # Delta de caudales antrópicos
        afl.append(a)  # Caudales afluentes
        efl.append(b)  # Caudales efluente
    return dq_ant, afl, efl
def potencial_de_renovacion(vol_sis, caudales_efl, con_ini=100):
    # Se calcula el potencial de renovación
    Potrev = []
    Cto = []
    for i in range(0, 365):
        if i < 364:
            Mo = con_ini * vol_sis[i]
            Ms = (caudales_efl[i] * con_ini) * 86400
            Mt = Mo - Ms
            Ct = Mt / vol_sis[i + 1]
            Pr = ((con_ini - Ct) / con_ini) * 100
        elif i == 365:
            Potrev = Potrev[i - 1]
            Ct = Cto[i - 1]
        Cto.append(Ct)
        Potrev.append(Pr)
    return Potrev
def potencial_de_deficit(niveles,niv_crit):
    #Se calcula el potencial de déficit hídrico
    Pdh=((niveles-niv_crit)/niv_crit)*100 #Potencial déficit hídrico calculado con el nivel simulado Lr critico
    return Pdh
def potencial_de_salinizacion(salinidad,con_geo=2.5,tem_geo=21.2):
    ps=[]
    sg=salinidad1(con_geo, tem_geo)
    for i in range(0,len(salinidad)):
        a=salinidad[i]/sg*100
        ps.append(a)
    return ps
def graficar(variable,fecha,ylabel,cota_rebose=0,color='#131C76',label='label'):
    if cota_rebose!=0:
        cota_desborde = [cota_rebose for i in range(0, len(fecha))]
        plt.plot(fecha, cota_desborde, color=str(color),label=str(label))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.plot(fecha,variable,color=str(color),label=str(label))
    plt.legend(loc='best')
    plt.gcf().autofmt_xdate()
    plt.grid(linestyle='--',linewidth ='0.5')
    plt.xlim(fecha[0],fecha[len(fecha)-1])
    plt.xticks(rotation=45,size='medium')
    plt.ylabel(str(ylabel),fontsize=14,**{'fontname':'Times new roman'})
    plt.xlabel('')
def NS(observados, modelados):  # índice Nash para calibración
    a = np.sum(np.square(modelados - observados))
    b = np.sum(np.square(observados)) - ((1 / len(observados)) * (np.sum(observados) ** 2))
    return 1 - (a / b)
def cambiar_formato(lista_variable,fechas):
    names = ['INST-VAL', 'M3/S', '', '', 'FLOW', 'ITP', 'RIO CHICAMOCHA']
    blanks = ['' for i in range(0, 7)]
    for i in range(0,len(blanks)):
        if i==0:
            a=np.insert(fechas,0,blanks[i])
        else:
            a=np.insert(a,0,blanks[i])
        fecha=a
    for name in range(0,len(names)):
        b=lista_variable[:]
        b.insert(0, names[name])
        lista_variable=b
    dss=pd.DataFrame()
    dss[0]=fecha
    dss[1]=lista_variable
    dss=dss.fillna('')
    return dss
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
        else:
            Bajo.append(posicion)
def clasificarPotencialSalinizacion(MuyAlto, Alto, Moderado, Bajo,
                                    Limite1, Limite2, Limite3, Serie):
    longitudSerie = len(Serie)
    for posicion in range(longitudSerie):
        if Serie[posicion] >= Limite1:
            MuyAlto.append(posicion)
        elif Serie[posicion] >= Limite2 and Serie[posicion] < Limite1:
            Alto.append(posicion)
        elif Serie[posicion] >= Limite3 and Serie[posicion] < Limite2:
            Moderado.append(posicion)
        else:
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
def grafica_OSI(fecha,serieOSI):
    OSIMA=[]
    OSIA=[]
    OSIM=[]
    OSIB=[]
    for i in range(longitudSerie):
        OSIMA.append(1)
        OSIA.append(2)
        OSIM.append(3)
        OSIB.append(4)
    plt.figure(figsize=(15,6))
    plt.plot(fecha, OSIB, color='b', label='Low')
    plt.plot(fecha, OSIM, color='y', label='Moderate')
    plt.plot(fecha, OSIA, color='#FF8000', label='High')
    plt.plot(fecha, OSIMA, color='r', label='Very High')
    plt.plot(fecha, serieOSI, 'ok', label='OSI')
    #Coloco la leyenda y la ubico con un tamaño específico
    plt.legend(loc='upper right',bbox_to_anchor=(1.12, 0.65), fontsize=10, shadow=True,borderpad=0.2)
    plt.grid(linestyle=':', linewidth='0.5')
    plt.xlim(fecha[0],fecha[len(fecha)-1])

    plt.ylabel('Overall susceptibility index (OSI)',fontweight='bold',fontsize=14, **{'fontname':'calibri'})
    plt.xticks(size='large',color ='k',rotation = 45,**{'fontname':'calibri'})
    plt.yticks(size='large',color ='k',rotation = 0,**{'fontname':'calibri'})
    #plt.savefig(ruta_imagenes+'\\'+str(año)+'_'+str(esc)+'.png')
def pie_chart(PorcentajeMuyAltoOSI, PorcentajeAltoOSI, PorcentajeBajoOSI, PorcentajeModeradoOSI):
    OSI = [PorcentajeMuyAltoOSI, PorcentajeAltoOSI, PorcentajeBajoOSI, PorcentajeModeradoOSI]

    labels = ['Very High', 'High', 'Low', 'Moderate']
    colores = ['red', '#FF8000', 'blue', 'yellow']
    explode = (0.1, 0.1, 0.1, 0.1)
    wp = {'linewidth': 1, 'edgecolor': "black"}
    plt.figure(figsize=(15, 6))
    wedges, texts, autotexts = plt.pie(OSI, labels=labels, autopct='%1.1f%%', startangle=15,
                                       shadow=True, colors=colores, explode=explode,
                                       textprops={'fontsize': 14, 'fontname': 'calibri'}, wedgeprops=wp)
    plt.legend(wedges, labels,
               loc="center left",
               bbox_to_anchor=(0.2, 1))
    plt.setp(autotexts, size=10)
    plt.axis('equal', **{'fontname': 'calibri'})
def grafica_climatologica(fecha,variable_1,variable_2,str1='Precipitation [mm]',str2='Evaporation [mm]'):
    fig = plt.figure(figsize=(15, 6))
    x = fecha
    plt.subplot(2, 1, 1)
    plt.plot(x, variable_1, color='#050DF4')
    plt.grid(linestyle=':', linewidth='0.5')
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    plt.ylabel(str1, fontsize=15, **{'fontname': 'calibri'})
    plt.xlabel('', fontsize=15, **{'fontname': 'calibri'})
    plt.xlim(fecha[0],fecha[len(fecha)-1])

    plt.subplot(2, 1, 2)
    plt.plot(x, variable_2, color='#050DF4')
    plt.grid(linestyle=':', linewidth='0.5')
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    plt.ylabel(str2, fontsize=15, **{'fontname': 'calibri'})
    plt.xlabel('', fontsize=15, **{'fontname': 'calibri'})
    plt.xlim(fecha[0], fecha[len(fecha) - 1])
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

def grafica_niveles_caudales(caudales,niveles,fecha,label1,label2):

    variable_1=caudales
    variable_2=niveles
    fig = plt.figure(figsize=(15, 6))
    x = fecha
    str1 = 'Flow [m3/s]'
    str2 = 'Water level [m]'
    plt.subplot(2, 1, 1)
    plt.plot(x, variable_1, color='#050DF4',label=str(label1))
    plt.grid(linestyle=':', linewidth='0.5')
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    plt.ylabel(str1,fontweight='bold', fontsize=15, **{'fontname': 'calibri'})
    plt.xlabel('', fontsize=15, **{'fontname': 'calibri'})
    plt.xlim(fecha[0],fecha[len(fecha)-1])
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(x, variable_2, color='#050DF4',label=str(label2))
    plt.grid(linestyle=':', linewidth='0.5')
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    plt.ylabel(str2,fontweight='bold', fontsize=15, **{'fontname': 'calibri'})
    plt.xlabel('', fontsize=15, **{'fontname': 'calibri'})
    plt.xlim(fecha[0], fecha[len(fecha) - 1])
    plt.legend()
    plt.tight_layout()
################## Dársena 1 ############################################################

fec1="01/01/2018"
fec2="12/31/2018" #Modificar fecha según periodo simulado
fecha=np.array(pd.date_range(fec1,fec2))

#Variables de entrada D1
ruta_carpeta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Darsena_1'
nombre_excel='Variables_de_entrada_Darsena_1'
Afluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Afluentes')
Efluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Efluentes')
Conductividad=Abrir_excel(ruta_carpeta,nombre_excel,'Conductividad')
Temperatura=Abrir_excel(ruta_carpeta,nombre_excel,'Temperatura')
# observados=Abrir_excel(ruta_carpeta,nombre_excel,'Datos_observados')
Horas_bombeo=Abrir_excel(ruta_carpeta,nombre_excel,'Horas_bombeo')

#Variables climáticas
nombre_excel='Evaporacion'
Evaporacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
nombre_excel='Precipitacion'
Precipitacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
Precipitacion=Precipitacion['Q. Seca'].loc[fec1:fec2]
Evaporacion=Evaporacion['Q. Seca'].loc[fec1:fec2]

#Calculo de alturas y caudal de salida de dársena 1
No=1.5
prec=Precipitacion
evap=Evaporacion
dq_ant,afl,efl=caudales_antropicos(Afluentes,Efluentes)
hor_bom=Horas_bombeo['Horas de bombeo']

Alturas_D1,Caudal_salida_D1,Areas_mod_D1=Dinamica_darsena_1(No,prec,evap,dq_ant,hor_bom)

Alturas_cal=pd.DataFrame(Alturas_D1) #Para calibración
Alturas_cal['Fecha']=fecha
Alturas_cal.set_index('Fecha',inplace=True)
Alturas_cal=Alturas_cal.rename(columns={0: "Modelados"})

# Alturas_cal.plot(figsize=(15,6),color='black',label='Modelados') #Para calibración
# # plt.plot(observados.index,observados[observados.columns[0]],color='red',label='Observados')
# plt.grid(linestyle='--',linewidth ='0.5')
# plt.legend()

# print('El índice de NASH es: ', round(NS(observados[observados.columns[0]],Alturas_cal['Modelados']),3))
graficar(Alturas_D1,fecha,'Niveles [m]')
plt.show()

graficar(Caudal_salida_D1,fecha,'Caudal [m3/s)')
plt.show()

#Potencial de salinidad

#Salinidad dársena 1
salinidad_D1=pd.DataFrame()
for j in range(0,Conductividad.shape[1]):
    b=[]
    for i in range(0,Conductividad.shape[0]):
        a=salinidad1(Conductividad.iloc[i,j],Temperatura.iloc[i,j])
        b.append(a)
    salinidad_D1[Conductividad.columns[j]]=b
salinidad_D1.index=Conductividad.index

#Cargas entrantes a la dársena 1, se realizando multiplicando cada caudal por cada concentración. Finalmente se suman todas las cargas
#diariamente
cargas=[]
for i in range(0,Afluentes.shape[0]):
    a=np.sum(salinidad_D1.iloc[i].values*Afluentes.iloc[i].values)
    cargas.append(a)
cargas_D1=np.array(cargas)

#Potencial de salinización de la dársena 1
vol_sis=Alturas_D1*Areas_mod_D1 #Se calcula el volumen de dársena 1 con cada nivel
cargas_afluentes=cargas_D1 #Se llaman las cargas de salinidades
caudales_efl=np.array(efl) #Se llaman los caudales efluentes
con_inicial=10.16
tem_inicial=20

#serie temporal de salinidad
Salinidad_efl_D1=salinizacion(vol_sis,cargas_afluentes,caudales_efl,con_inicial,tem_inicial)
cargas_salida_D1=Salinidad_efl_D1*Caudal_salida_D1


#Calculo de los potenciales
pot_rev=potencial_de_renovacion(vol_sis,caudales_efl)
pot_def_hid=potencial_de_deficit(Alturas_D1,2.20)
pot_sal=potencial_de_salinizacion(Salinidad_efl_D1,0.1287,17.15)

#Calculo de potenciales
#Potencial de déficit hídrico
# Establezco Serie y límites
SeriePwd = pot_def_hid
LimitePWd1 = -36.4
LimitePWd2 = -12.78
LimitePWd3 = 11.45
longitudSerie = len(SeriePwd)

# Definición de categorias
MuyAltoPWd = []
AltoPWd = []
ModeradoPWd = []
BajoPWd = []

# Invoco función clasificarPotencial
clasificarPotencial(MuyAltoPWd, AltoPWd, ModeradoPWd, BajoPWd, LimitePWd1, LimitePWd2, LimitePWd3, SeriePwd)

# Invoco función hallar porcentaje por categoría
porcentajes = hallarPorcentajeCategoria(MuyAltoPWd, AltoPWd, ModeradoPWd, BajoPWd, longitudSerie)

# Asigno cada porcentaje
PorcentajeMuyAltoPWd = porcentajes[0]
PorcentajeAltoPWd = porcentajes[1]
PorcentajeModeradoPWd = porcentajes[2]
PorcentajeBajoPWd = porcentajes[3]

# InvocoFunción para hallar concepto Global
conceptoGlobalPWd = hallarConceptoGlobal(PorcentajeMuyAltoPWd, PorcentajeAltoPWd, PorcentajeModeradoPWd,
                                         PorcentajeBajoPWd)

print("Déficit hídrico D1:" + str(conceptoGlobalPWd))
print("Muy Alto: " + str(PorcentajeMuyAltoPWd) + str("%"))
print("Alto: " + str(PorcentajeAltoPWd) + str("%"))
print("Moderado: " + str(PorcentajeModeradoPWd) + str("%"))
print("Bajo: " + str(PorcentajeBajoPWd) + str("%"))

#Potencial de renovación

# Establezco Serie y límites
SeriePR = pot_rev
LimitePR1 = -41.56
LimitePR2 = -25.91
LimitePR3 = 3.65
longitudSerie = len(SeriePR)

# Definición de categorias
MuyAltoPR = []
AltoPR = []
ModeradoPR = []
BajoPR = []

# Invoco función clasificarPotencial
clasificarPotencial(MuyAltoPR, AltoPR, ModeradoPR, BajoPR, LimitePR1, LimitePR2, LimitePR3, SeriePR)

# Invoco función hallar porcentaje por categoría
porcentajes = hallarPorcentajeCategoria(MuyAltoPR, AltoPR, ModeradoPR, BajoPR, longitudSerie)

# Asigno cada porcentaje
PorcentajeMuyAltoPR = porcentajes[0]
PorcentajeAltoPR = porcentajes[1]
PorcentajeModeradoPR = porcentajes[2]
PorcentajeBajoPR = porcentajes[3]

# InvocoFunción para hallar concepto Global
conceptoGlobalPR = hallarConceptoGlobal(PorcentajeMuyAltoPR, PorcentajeAltoPR, PorcentajeModeradoPR, PorcentajeBajoPR)

print("Potencial de renovación D1:" + str(conceptoGlobalPR))
print("Muy Alto: " + str(PorcentajeMuyAltoPR) + str("%"))
print("Alto: " + str(PorcentajeAltoPR) + str("%"))
print("Moderado: " + str(PorcentajeModeradoPR) + str("%"))
print("Bajo: " + str(PorcentajeBajoPR) + str("%"))

#Potencial de salinización
SeriePS = pot_sal
LimitePS1 = -68
LimitePS2 = -83
LimitePS3 = -98.41
longitudSerie = len(SeriePS)

# Definición de categorias
MuyAltoPS = []
AltoPS = []
ModeradoPS = []
BajoPS = []

# Invoco función clasificarPotencial
clasificarPotencialSalinizacion(MuyAltoPS, AltoPS, ModeradoPS, BajoPS, LimitePS1, LimitePS2, LimitePS3, SeriePS)

# Invoco función hallar porcentaje por categoría
porcentajes = hallarPorcentajeCategoria(MuyAltoPS, AltoPS, ModeradoPS, BajoPS, longitudSerie)

# Asigno cada porcentaje
PorcentajeMuyAltoPS = porcentajes[0]
PorcentajeAltoPS = porcentajes[1]
PorcentajeModeradoPS = porcentajes[2]
PorcentajeBajoPS = porcentajes[3]

# InvocoFunción para hallar concepto Global
conceptoGlobalPS = hallarConceptoGlobal(PorcentajeMuyAltoPS, PorcentajeAltoPS, PorcentajeModeradoPS, PorcentajeBajoPS)

print("Potencial de salinización D1:" + str(conceptoGlobalPS))
print("Muy Alto: " + str(PorcentajeMuyAltoPS) + str("%"))
print("Alto: " + str(PorcentajeAltoPS) + str("%"))
print("Moderado: " + str(PorcentajeModeradoPS) + str("%"))
print("Bajo: " + str(PorcentajeBajoPS) + str("%"))

#Cálculo de OSI

OPR=[]
OPs=[]
OPd=[]
OSI=[]
#PotencialRenovación
insertarDatosPotencialOSI(MuyAltoPR, AltoPR, ModeradoPR, BajoPR, OPR)
#PotencialSalinizacion
insertarDatosPotencialOSI(MuyAltoPS, AltoPS, ModeradoPS, BajoPS, OPs)
#Potencial Déficit
insertarDatosPotencialOSI(MuyAltoPWd, AltoPWd, ModeradoPWd, BajoPWd, OPd)
#Invoco generarOSI
print('revisar: ',len(OPR),len(OPs),len(OPd))
serieOSI=generarDatosOSI(OPR, OPs, OPd)
#print(serieOSI)

#----Algoritmo OSI
longitudSerie=len(serieOSI)

#Definición de categorias
MuyAltoOSI=[]
AltoOSI=[]
ModeradoOSI=[]
BajoOSI=[]

#Invoco función clasificarPotencial
clasificarPotencial(MuyAltoOSI, AltoOSI, ModeradoOSI, BajoOSI, 1, 2, 3, serieOSI)

#Invoco función hallar porcentaje por categoría
porcentajes = hallarPorcentajeCategoria(MuyAltoOSI, AltoOSI, ModeradoOSI, BajoOSI, longitudSerie)

#Asigno cada porcentaje
PorcentajeMuyAltoOSI=porcentajes[0]
PorcentajeAltoOSI=porcentajes[1]
PorcentajeModeradoOSI=porcentajes[2]
PorcentajeBajoOSI=porcentajes[3]

#InvocoFunción para hallar concepto Global
conceptoGlobalOSI=hallarConceptoGlobal(PorcentajeMuyAltoOSI, PorcentajeAltoOSI, PorcentajeModeradoOSI, PorcentajeBajoOSI)

print("Concepto Global OSI D1:"+ str(conceptoGlobalOSI))
print("Muy Alto: " + str(PorcentajeMuyAltoOSI) + str("%"))
print("Alto: " + str(PorcentajeAltoOSI) + str("%"))
print("Moderado: " + str(PorcentajeModeradoOSI) + str("%"))
print("Bajo: " + str(PorcentajeBajoOSI) + str("%"))

ruta_guardado=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Resultados\Darsenas\Darsena_1'
grafica_climatologica(fecha,prec,evap)
# plt.savefig('climatologia_2011.png')
plt.show()
graficar_potencial(fecha, pot_rev, LimitePR1, LimitePR2, LimitePR3, potencial='renovación',label='Renewal potential')
plt.savefig(ruta_guardado+'\\'+'Potencial_de_renovacion_2018_D1.png')
plt.show()
graficar_potencial(fecha, pot_sal, LimitePS1,LimitePS2, LimitePS3, potencial='salinizacion',label='Salinization potential')
plt.savefig(ruta_guardado+'\\'+'Potencial_de_salinizacion_2018_D1.png')
plt.show()
graficar_potencial(fecha, pot_def_hid, LimitePWd1, LimitePWd2, LimitePWd3, potencial='deficit hidrico',label='Water deficit potential')
plt.savefig(ruta_guardado+'\\'+'Potencial_de_deficit_2018_D1.png')
plt.show()
grafica_OSI(fecha,serieOSI)
plt.savefig(ruta_guardado+'\\'+'OSI_2018_D1.png')
plt.show()

Alturas_D1=[Alturas_D1[i]+2487.25 for i in range(0,len(Alturas_D1))]

grafica_niveles_caudales(Caudal_salida_D1,Alturas_D1,fecha,'Efluent from Dársena 1','Dársena 1')
# graficar(Alturas_D1,fecha,'Water level [m]',label='Dársena 1')
plt.savefig(ruta_guardado+'\\'+'D1_niveles.png')
plt.show()
# graficar(Caudal_salida_D1,fecha,'Flow [m3/s]',label='Efluent from D1')
# plt.savefig(ruta_guardado+'\\'+'D1_caudales.png')
# plt.show()

#Se convierten en formato DSS
DSS_salD1=cambiar_formato(Salinidad_efl_D1,fecha)
DSS_cauD1=cambiar_formato(list(Caudal_salida_D1),fecha)
#Se exportan a Excel
DSS_salD1.to_excel(ruta_guardado+'\Salinidad_D1.xls',index=False,header=False)
DSS_cauD1.to_excel(ruta_guardado+'\Efluentes_D1.xls',index=False,header=False)
#################################### Dársena 2 ################################################

fec1="01/01/2018"
fec2="12/31/2018" #Modificar fecha según periodo simulado
fecha=np.array(pd.date_range(fec1,fec2))

#Variables de entrada D2
ruta_carpeta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Darsena_2'
nombre_excel='Variables_de_entrada_Darsena_2'
Afluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Afluentes')
Efluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Efluentes')
Conductividad=Abrir_excel(ruta_carpeta,nombre_excel,'Conductividad')
Temperatura=Abrir_excel(ruta_carpeta,nombre_excel,'Temperatura')
#observados=Abrir_excel(ruta_carpeta,nombre_excel,'Datos_observados')
Compuerta=Abrir_excel(ruta_carpeta,nombre_excel,'Compuerta')

#Variables climáticas
nombre_excel='Evaporacion'
# Evaporacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
nombre_excel='Precipitacion'
# Precipitacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
# Precipitacion=Precipitacion['Q. Seca'].loc[fec1:fec2]
# Evaporacion=Evaporacion['Q. Seca'].loc[fec1:fec2]

#Calculo de altura y caudal de dársena 2
No=1.4
Cfl=2497.16
Cfc=2497.86
prec=Precipitacion
evap=Evaporacion
dq_ant,afl,efl=caudales_antropicos(Afluentes,Efluentes)
aper_com=Compuerta['Porcentaje de apertura (%)']
cau_dar1=Caudal_salida_D1

Alturas_D2,Caudal_salida_D2,Areas_mod_D2=Dinamica_Darsena2(No,Cfl,Cfc,prec,evap,dq_ant,cau_dar1,aper_com)

# Alturas_cal=pd.DataFrame(Alturas_D2) #Para calibración
# Alturas_cal['Fecha']=fecha
# Alturas_cal.set_index('Fecha',inplace=True)
# Alturas_cal=Alturas_cal.rename(columns={0: "Modelados"})
#
# Alturas_cal.plot(figsize=(15,6),color='black',label='Modelados') #Para calibración
# #plt.scatter(x=observados.index,y=observados[observados.columns[0]],s=8,color='red',label='Observados')
# #observados[observados.columns[0]].plot()
# plt.grid(linestyle='--',linewidth ='0.5')
# plt.legend()

graficar(Alturas_D2,fecha,'Niveles [m]')
plt.show()

graficar(Caudal_salida_D2,fecha,'Caudal [m3/s)')
plt.show()

#Potencial de salinidad
#Salinidad dársena 2
salinidad_D2=pd.DataFrame()
for j in range(0,Conductividad.shape[1]):
    b=[]
    for i in range(0,Conductividad.shape[0]):
        a=salinidad1(Conductividad.iloc[i,j],Temperatura.iloc[i,j])
        b.append(a)
    salinidad_D2[Conductividad.columns[j]]=b
salinidad_D2.index=Conductividad.index

plt.show()

#Cargas entrantes a la dársena 2, se realizando multiplicando cada caudal por cada concentración. Finalmente se suman todas las cargas
#diariamente
cargas=[]
for i in range(0,Afluentes.shape[0]):
    a=np.sum(salinidad_D2.iloc[i].values*Afluentes.iloc[i].values)
    cargas.append(a)
cargas=np.array(cargas+cargas_salida_D1)  #Se suma adicionalmente la carga proveniente de Darsena 1

#Potencial de salinización de la dársena 2
vol_sis=Alturas_D2*Areas_mod_D2 #Se calcula el volumen de dársena 2 con cada nivel
cargas_afluentes=cargas #Se llaman las cargas de salinidades
caudales_efl=np.array(efl) #Se llaman los caudales efluentes
con_inicial=10.16
tem_inicial=20

#serie temporal de salinidad
Salinidad_efl_D2=salinizacion(vol_sis,cargas_afluentes,caudales_efl,con_inicial,tem_inicial)
#Salidas Caudal_salida_D2, salinidad_D2
# print(cambiar_formato(Salinidad_efl_D2,fecha))

#Calculo de los potenciales
pot_rev=potencial_de_renovacion(vol_sis,caudales_efl)
pot_def_hid=potencial_de_deficit(Alturas_D2,1.81)
pot_sal=potencial_de_salinizacion(Salinidad_efl_D2,0.1287,17.15)

#Calculo de potenciales
#Potencial de déficit hídrico
# Establezco Serie y límites
SeriePwd = pot_def_hid
LimitePWd1 = -24.46
LimitePWd2 = -14.98
LimitePWd3 = 3.38
longitudSerie = len(SeriePwd)

# Definición de categorias
MuyAltoPWd = []
AltoPWd = []
ModeradoPWd = []
BajoPWd = []

# Invoco función clasificarPotencial
clasificarPotencial(MuyAltoPWd, AltoPWd, ModeradoPWd, BajoPWd, LimitePWd1, LimitePWd2, LimitePWd3, SeriePwd)

# Invoco función hallar porcentaje por categoría
porcentajes = hallarPorcentajeCategoria(MuyAltoPWd, AltoPWd, ModeradoPWd, BajoPWd, longitudSerie)

# Asigno cada porcentaje
PorcentajeMuyAltoPWd = porcentajes[0]
PorcentajeAltoPWd = porcentajes[1]
PorcentajeModeradoPWd = porcentajes[2]
PorcentajeBajoPWd = porcentajes[3]

# InvocoFunción para hallar concepto Global
conceptoGlobalPWd = hallarConceptoGlobal(PorcentajeMuyAltoPWd, PorcentajeAltoPWd, PorcentajeModeradoPWd,
                                         PorcentajeBajoPWd)

print("Déficit hídrico D2:" + str(conceptoGlobalPWd))
print("Muy Alto: " + str(PorcentajeMuyAltoPWd) + str("%"))
print("Alto: " + str(PorcentajeAltoPWd) + str("%"))
print("Moderado: " + str(PorcentajeModeradoPWd) + str("%"))
print("Bajo: " + str(PorcentajeBajoPWd) + str("%"))

#Potencial de renovación

# Establezco Serie y límites
SeriePR = pot_rev
LimitePR1 = -22.79
LimitePR2 = -5.45
LimitePR3 = 5.88
longitudSerie = len(SeriePR)

# Definición de categorias
MuyAltoPR = []
AltoPR = []
ModeradoPR = []
BajoPR = []

# Invoco función clasificarPotencial
clasificarPotencial(MuyAltoPR, AltoPR, ModeradoPR, BajoPR, LimitePR1, LimitePR2, LimitePR3, SeriePR)

# Invoco función hallar porcentaje por categoría
porcentajes = hallarPorcentajeCategoria(MuyAltoPR, AltoPR, ModeradoPR, BajoPR, longitudSerie)

# Asigno cada porcentaje
PorcentajeMuyAltoPR = porcentajes[0]
PorcentajeAltoPR = porcentajes[1]
PorcentajeModeradoPR = porcentajes[2]
PorcentajeBajoPR = porcentajes[3]

# InvocoFunción para hallar concepto Global
conceptoGlobalPR = hallarConceptoGlobal(PorcentajeMuyAltoPR, PorcentajeAltoPR, PorcentajeModeradoPR, PorcentajeBajoPR)

print("Potencial de renovación D2:" + str(conceptoGlobalPR))
print("Muy Alto: " + str(PorcentajeMuyAltoPR) + str("%"))
print("Alto: " + str(PorcentajeAltoPR) + str("%"))
print("Moderado: " + str(PorcentajeModeradoPR) + str("%"))
print("Bajo: " + str(PorcentajeBajoPR) + str("%"))

#Potencial de salinización
SeriePS = pot_sal
LimitePS1 = 6
LimitePS2 = -43
LimitePS3 = -94.82
longitudSerie = len(SeriePS)

# Definición de categorias
MuyAltoPS = []
AltoPS = []
ModeradoPS = []
BajoPS = []

# Invoco función clasificarPotencial
clasificarPotencialSalinizacion(MuyAltoPS, AltoPS, ModeradoPS, BajoPS, LimitePS1, LimitePS2, LimitePS3, SeriePS)

# Invoco función hallar porcentaje por categoría
porcentajes = hallarPorcentajeCategoria(MuyAltoPS, AltoPS, ModeradoPS, BajoPS, longitudSerie)

# Asigno cada porcentaje
PorcentajeMuyAltoPS = porcentajes[0]
PorcentajeAltoPS = porcentajes[1]
PorcentajeModeradoPS = porcentajes[2]
PorcentajeBajoPS = porcentajes[3]

# InvocoFunción para hallar concepto Global
conceptoGlobalPS = hallarConceptoGlobal(PorcentajeMuyAltoPS, PorcentajeAltoPS, PorcentajeModeradoPS, PorcentajeBajoPS)

print("Potencial de salinización D2:" + str(conceptoGlobalPS))
print("Muy Alto: " + str(PorcentajeMuyAltoPS) + str("%"))
print("Alto: " + str(PorcentajeAltoPS) + str("%"))
print("Moderado: " + str(PorcentajeModeradoPS) + str("%"))
print("Bajo: " + str(PorcentajeBajoPS) + str("%"))

#Cálculo de OSI

OPR=[]
OPs=[]
OPd=[]
OSI=[]
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
MuyAltoOSI=[]
AltoOSI=[]
ModeradoOSI=[]
BajoOSI=[]

#Invoco función clasificarPotencial
clasificarPotencial(MuyAltoOSI, AltoOSI, ModeradoOSI, BajoOSI, 1, 2, 3, serieOSI)

#Invoco función hallar porcentaje por categoría
porcentajes = hallarPorcentajeCategoria(MuyAltoOSI, AltoOSI, ModeradoOSI, BajoOSI, longitudSerie)

#Asigno cada porcentaje
PorcentajeMuyAltoOSI=porcentajes[0]
PorcentajeAltoOSI=porcentajes[1]
PorcentajeModeradoOSI=porcentajes[2]
PorcentajeBajoOSI=porcentajes[3]

#InvocoFunción para hallar concepto Global
conceptoGlobalOSI=hallarConceptoGlobal(PorcentajeMuyAltoOSI, PorcentajeAltoOSI, PorcentajeModeradoOSI, PorcentajeBajoOSI)

print("Concepto Global OSI D2:"+ str(conceptoGlobalOSI))
print("Muy Alto: " + str(PorcentajeMuyAltoOSI) + str("%"))
print("Alto: " + str(PorcentajeAltoOSI) + str("%"))
print("Moderado: " + str(PorcentajeModeradoOSI) + str("%"))
print("Bajo: " + str(PorcentajeBajoOSI) + str("%"))

grafica_climatologica(fecha,prec,evap)
# plt.savefig('climatologia_2011.png')
plt.show()
ruta_guardado=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Simulacion_global\Base\Resultados\Darsenas\Darsena_2'
graficar_potencial(fecha, pot_rev, LimitePR1, LimitePR2, LimitePR3, potencial='renovación',label='Renewal potential')
plt.savefig(ruta_guardado+'\\'+'Potencial_de_renovacion_2018_D2.png')
plt.show()
graficar_potencial(fecha, pot_sal, LimitePS1,LimitePS2, LimitePS3, potencial='salinizacion',label='Salinization potential')
plt.savefig(ruta_guardado+'\\'+'Potencial_de_salinizacion_2018_D2.png')
plt.show()
graficar_potencial(fecha, pot_def_hid, LimitePWd1, LimitePWd2, LimitePWd3, potencial='deficit hidrico',label='Water deficit potential')
plt.savefig(ruta_guardado+'\\'+'Potencial_de_deficit_2018_D2.png')
plt.show()
grafica_OSI(fecha,serieOSI)
plt.savefig(ruta_guardado+'\\'+'OSI_2011_D2.png')
plt.show()

Alturas_D2=[Alturas_D2[i]+2497.80 for i in range(0,len(Alturas_D1))]
grafica_niveles_caudales(Caudal_salida_D2,Alturas_D2,fecha,'Efluent from Dársena 2','Dársena 2')
# graficar(Alturas_D2,fecha,'Water level [m]',label='Dársena 2')
plt.savefig(ruta_guardado+'\\'+'D2_niveles.png')
plt.show()
# graficar(Caudal_salida_D2,fecha,'Flow [m3/s]',label='Efluent from D2')
# plt.savefig(ruta_guardado+'\\'+'D2_caudales.png')
# plt.show()


#Se convierte a DSS
DSS_sal=cambiar_formato(Salinidad_efl_D2,fecha)
DSS_cau=cambiar_formato(list(Caudal_salida_D2),fecha)

#Se exportan los resultados a Excel
DSS_sal.to_excel(ruta_guardado+'\Salinidad_D2.xls',index=False,header=False)
DSS_cau.to_excel(ruta_guardado+'\Efluentes_D2.xls',index=False,header=False)
