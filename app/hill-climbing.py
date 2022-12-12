import pandas as pd
import numpy as np
import random
import plotly.figure_factory as ff
from datetime import datetime,timedelta
TODAY = datetime(2022,1,1,0,0,0)
def evaluate_solution(jobs,resourcesEl,resourcesOr,solution,Elixir,Oro,reg):
    #create list with length of resources
    trabajos=[0]*len(jobs.columns)
    maquinas=[0]*5
    porsec=reg/60
    df=[]
    key_count={i:0 for i in range(len(jobs.columns))}
    for i in range(0,len(solution)):
        operacion=solution[i]
        tiemp=int(jobs.iloc[key_count[operacion],operacion])
        maquina=np.argmin(maquinas)
        boole=False
        if(resourcesEl.iloc[key_count[operacion],operacion]!='None'):
            if int(resourcesEl.iloc[key_count[operacion],operacion])>Elixir:
                recursosfaltantes=int(resourcesEl.iloc[key_count[operacion],operacion])-Elixir
                tiempoextra=recursosfaltantes/porsec
                tiemp+=int(tiempoextra)+1
                Elixir=0
                boole=True
            else:
                Elixir-=int(resourcesEl.iloc[key_count[operacion],operacion])
        if(resourcesOr.iloc[key_count[operacion],operacion]!='None'):
            if int(resourcesOr.iloc[key_count[operacion],operacion])>Oro:
                recursosfaltantes=int(resourcesOr.iloc[key_count[operacion],operacion])-Oro
                tiempoextra=recursosfaltantes/porsec
                tiemp+=int(tiempoextra)+1
                Oro=0
                boole=True
            else:
                Oro-=int(resourcesOr.iloc[key_count[operacion],operacion])
        maquinas[maquina]+=int(tiemp)
        trabajos[operacion]+=int(tiemp)
        if(maquinas[maquina]>trabajos[operacion]):
            trabajos[operacion]=maquinas[maquina]
        else:
            maquinas[maquina]=trabajos[operacion]
        key_count[operacion]+=1
        if(boole):
            print(tiemp,tiempoextra)
            #start = dia de hoy mas segundos de maquina menos tiempo de trabajo mas tiempo extra
            #finish = dia de hoy mas segundos de maquina
            df.append(dict(Task="T"+str(maquina), Start=TODAY+timedelta(seconds=int(maquinas[maquina]-tiemp+tiempoextra)), Finish=TODAY+timedelta(seconds=int(maquinas[maquina])), Resource=jobs.columns[operacion]))
            print("trabajador "+str(maquina)+" Start:"+str(maquinas[maquina]-tiemp+tiempoextra)+" Finish:"+str(maquinas[maquina])+" "+jobs.columns[operacion])
        else:
            df.append(dict(Task="T"+str(maquina), Start=TODAY+timedelta(seconds=int(maquinas[maquina]-tiemp)), Finish=TODAY+timedelta(seconds=int(maquinas[maquina])), Resource=jobs.columns[operacion]))
            print("trabajador "+str(maquina)+" Start:"+str(maquinas[maquina]-tiemp)+" Finish:"+str(maquinas[maquina])+" "+jobs.columns[operacion])
    print(df)
    return df
def hill_climbing(solucion_inicial):
    return 0

        

tiempos=pd.read_csv('./test/Tiempos.csv',sep=';',index_col=0)
recursosOro=pd.read_csv('./test/Recursos-Oro.csv',sep=';',index_col=0)
recursosEl=pd.read_csv('./test/Recursos-Elixir.csv',sep=';',index_col=0)
solucion=[4, 1, 6, 0, 5, 3, 5, 4, 1, 1, 1, 3, 2]
random.shuffle(solucion)
print(solucion)
df=evaluate_solution(tiempos,recursosEl,recursosOro,solucion,1000,1000,45)


# Crea una lista con los tiempos en el eje x
# (inicio y fin de cada período)
time = [(0, 15), (15, 35), (35, 40), (40, 120), (120, 140)]

# Crea una lista con los estados en el eje y
# (1 para trabajo y 0 para tiempo muerto)
status = [1, 0, 1, 0, 1]

# Dibuja la línea de tiempo utilizando el método broken_barh()



colors = {i: f'rgb({random.randint(0,255)},{random.randint(0,255)}, {random.randint(0,255)})' for i in tiempos.columns}

fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                      group_tasks=True)
fig.show()

  


