import pandas as pd
import numpy as np
import random
import plotly.figure_factory as ff
from datetime import datetime,timedelta
import itertools
TODAY = datetime(2022,1,1,0,0,0)

def conocerlevels(time):
    key_count={i:0 for i in range(len(time.columns))}
    for i in range(0,len(time)):
        for j in range(0,len(time.columns)):
            if(time.iloc[i,j]!='None'):
                key_count[j]+=1
    print(key_count)
    return key_count

def usaelixirooro(name,resiurcesOr):
    if name in resiurcesOr.columns:
        return True
    else:
        return False



def evaluate_solution(jobs,resourcesEl,resourcesOr,solution,Elixir,Oro,reg):
    trabajos=[0]*len(jobs.columns)
    maquinas=[0]*5
    porsec=reg/60
    df=[]
    
    key_count=conocerlevels(jobs)
    for i in range(0,len(solution)):
        operacion=solution[i]
        tiemp=int(jobs.iloc[key_count[operacion],operacion])
        maquina=np.argmin(maquinas)
        boole=False
        orooo=usaelixirooro(jobs.columns[operacion],resourcesOr)
        if orooo==False:
            if(resourcesEl.iloc[key_count[operacion],operacion]!='None'):
                if int(resourcesEl.iloc[key_count[operacion],operacion])>Elixir:
                    recursosfaltantes=int(resourcesEl.iloc[key_count[operacion],operacion])-Elixir
                    tiempoextra=recursosfaltantes/porsec
                    tiemp+=int(tiempoextra)+1
                    Elixir=0
                    boole=True
                else:
                    Elixir-=int(resourcesEl.iloc[key_count[operacion],operacion])
        else:
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
            df.append(dict(Task="T"+str(maquina), Start=TODAY+timedelta(seconds=int(maquinas[maquina]-tiemp+tiempoextra)), Finish=TODAY+timedelta(seconds=int(maquinas[maquina])), Resource=jobs.columns[operacion]))
        else:
            df.append(dict(Task="T"+str(maquina), Start=TODAY+timedelta(seconds=int(maquinas[maquina]-tiemp)), Finish=TODAY+timedelta(seconds=int(maquinas[maquina])), Resource=jobs.columns[operacion]))
    return max(trabajos)



def operadormovimiento(solucion):
    combinaciones = []
    for i in range(len(solucion)):
        for j in range(len(solucion)):
            if i != j:
                permutacion=solucion.copy()
                permutacion[i],permutacion[j]=permutacion[j],permutacion[i] 
                combinaciones.append(permutacion)
    return combinaciones


def hill_climbing(solucion_inicial,tiempos,recursosEl,recursosOro):
    optimo=9999999999999999999999
    solucion=solucion_inicial
    iteraciones=0
    while iteraciones<10:
        mejor_vecino=None
        for vecino in operadormovimiento(solucion):
            valor=evaluate_solution(tiempos,recursosEl,recursosOro,vecino,1000,1000,45)
            if valor<optimo:
                print("mejoro la solucion")
                print(optimo,valor)
                optimo=valor
                mejor_vecino=vecino
        if mejor_vecino!=None:
            solucion=mejor_vecino
        iteraciones+=1
    return mejor_vecino
def solucion_init(jobs):
    solucion=[]
    contador=0
    for i in jobs.columns:
        for j in jobs[i]:
            if j!="None":
                solucion.append(contador)
        contador+=1
    print(solucion)
    random.shuffle(solucion)
    return solucion

def main():
    tiempos=pd.read_csv('./test/2_time.csv',sep=',',index_col=0)
    recursosOro=pd.read_csv('./test/2_gold.csv',sep=';',index_col=0)
    recursosEl=pd.read_csv('./test/2_elixir.csv',sep=';',index_col=0)
    solucion_init(tiempos)
    # df=evaluate_solution(tiempos,recursosEl,recursosOro,solucion,1000,1000,45)

    # colors = {i: f'rgb({random.randint(0,255)},{random.randint(0,255)}, {random.randint(0,255)})' for i in tiempos.columns}

    # fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
    #                     group_tasks=True)
    # fig.show()

if __name__ == '__main__':
    main()


