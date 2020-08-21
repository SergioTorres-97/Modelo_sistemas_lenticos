import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pl

ruta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Analisis_de_sensibilidad\Sensivity_analysis.xlsx'
ruta_imagen=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\Analisis_de_sensibilidad'

analisis=pd.read_excel(ruta,sheet_name='Analisis_de_sensibilidad',header=0,usecols='A:H')

nombres=np.unique(analisis[analisis.columns[0]])
variables=np.unique(analisis[analisis.columns[analisis.shape[1]-1]])
porcentajes=[-30,-20,-10,10,20,30]
originales=[0.558,0.996,199.823]

f=[]
for nombre in range(0,len(nombres)):
    b=(analisis.loc[analisis[analisis.columns[0]]==nombres[nombre]]).transpose()
    a=np.array(b)[1:-1].T
    plt.figure(figsize=(7, 5))
    g=[]
    for variable in range(0,len(a)):
        n = []
        for porcentaje in range(0,len(porcentajes)):
            n.append((((originales[nombre]-a[variable][porcentaje])/(originales[nombre]))*100)/(porcentajes[porcentaje]))
        colors = pl.cm.jet(np.linspace(0, 1,len(a)))
        plt.plot(porcentajes,a[variable]/originales[nombre],'o-',label=str(np.array(b)[-1][variable]),
                 markersize=3,color=colors[variable])
        plt.xlim(-30,30)
        plt.ylabel(str(nombres[nombre])+' change percentage [%]',fontsize=15,
                   fontweight='bold',**{'fontname': 'calibri'})
        plt.xlabel('Percentage of parameters variation [%]', fontsize=15,
                   fontweight='bold', **{'fontname': 'calibri'})
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5')
        plt.grid(which='minor', linestyle=':', linewidth='0.5')
        plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
        plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})

        lgd=plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5),prop={'size':10})
        g.append(sum(n)/len(n))
    f.append(g)
    plt.savefig(ruta_imagen + '\\' + str(nombres[nombre]) + '.png',
                dpi=500, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()


resultados=pd.DataFrame(np.array(f).T)
resultados.columns=nombres
resultados.index=variables[::-1]
resultados.to_excel(ruta_imagen+'\\'+'Resultados_sensibilidad.xlsx')
print(resultados)


