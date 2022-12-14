import pandas as pd
import numpy as np
import random
import plotly.figure_factory as ff
from datetime import datetime,timedelta
import itertools
import matplotlib.pyplot as plt
import time
TODAY = datetime(2022,1,1,0,0,0)

#igual que la funcion de evaluar pero entrega los datos para poder graficarlos
def grafico(jobs,resourcesEl,resourcesOr,solution,Elixir,Oro,reg):
    trabajos=[0]*len(jobs.columns)
    maquinas=[0]*5
    porsec=(reg/60)/60
    df=[]
    key_count=conocerlevels(jobs)
    for i in range(0,len(solution)):
        operacion=solution[i]
        tiemp=int(jobs.iloc[key_count[operacion],operacion])
        maquina=np.argmin(maquinas)
        boole=False
        orooo=usaelixirooro(jobs.columns[operacion],resourcesOr)  
        if orooo==False:
            recurso=resourcesEl[jobs.columns[operacion]].values[key_count[operacion]]
            if(recurso!='None'):
                if int(recurso)>Elixir:
                    recursosfaltantes=int(recurso)-Elixir
                    tiempoextra=recursosfaltantes/porsec
                    tiemp+=int(tiempoextra)+1
                    Elixir=0
                    boole=True
                else:
                    Elixir-=int(recurso)
        else:
            recurso=resourcesOr[jobs.columns[operacion]].values[key_count[operacion]]
            if(recurso!='None'):
                if int(recurso)>Oro:
                    recursosfaltantes=int(recurso)-Oro
                    tiempoextra=recursosfaltantes/porsec
                    tiemp+=int(tiempoextra)+1
                    Oro=0
                    boole=True
                else:
                    Oro-=int(recurso)
        maquinas[maquina]+=int(tiemp)
        trabajos[operacion]+=int(tiemp)
        if(maquinas[maquina]>trabajos[operacion]):
            trabajos[operacion]=maquinas[maquina]
        else:
            maquinas[maquina]=trabajos[operacion]
        key_count[operacion]+=1
        #aca se agregan los datos para graficar, se debe agregar el nombre de la maquina, el tiempo de inicio, el tiempo de finalizacion y el nombre de la tarea
        if(boole):
            df.append(dict(Task="T"+str(maquina), Start=TODAY+timedelta(seconds=int(maquinas[maquina]-tiemp+tiempoextra)), Finish=TODAY+timedelta(seconds=int(maquinas[maquina])), Resource=jobs.columns[operacion]))
        else:
            df.append(dict(Task="T"+str(maquina), Start=TODAY+timedelta(seconds=int(maquinas[maquina]-tiemp)), Finish=TODAY+timedelta(seconds=int(maquinas[maquina])), Resource=jobs.columns[operacion]))
    return df

#entrega un diccionario con los niveles de cada edificio con el que deben iniciar
def conocerlevels(time):
    key_count={i:0 for i in range(len(time.columns))}
    for i in time.columns:
        for j in time[i]:
            if j=="None":
                key_count[time.columns.get_loc(i)]+=1
            else:
                break
    return key_count
#conocer el edicicio que se debe construir requiere oro o elixir
def usaelixirooro(name,resiurcesOr):
    if name in resiurcesOr.columns:
        return True
    else:
        return False


#funcion para calcular el makespan de la solucion entregada
def evaluate_solution(jobs,resourcesEl,resourcesOr,solution,Elixir,Oro,reg):
    #inicializar 2 colas 1 para los trabajos y otra para las maquinas que llevaran el tiempo
    trabajos=[0]*len(jobs.columns)
    maquinas=[0]*5
    porsec=(reg/60)/60#cantidad de oro o elixir que se obtiene por segundo
    df=[]
    key_count=conocerlevels(jobs)
    #recorrer la solucion
    for i in range(0,len(solution)):
        #obtener que operacion es, el tiempo, en que maquina se ejecutara y si se debe usar oro o elixir
        operacion=solution[i]
        tiemp=int(jobs.iloc[key_count[operacion],operacion])
        maquina=np.argmin(maquinas)
        boole=False
        orooo=usaelixirooro(jobs.columns[operacion],resourcesOr)
        #si se debe usar elixir
        if orooo==False:
            #obtener la cantidad de recurso que se debe usar
            recurso=resourcesEl[jobs.columns[operacion]].values[key_count[operacion]]
            if(recurso!='None'):
                #si no se tiene suficiente recurso se debe esperar a que se obtenga
                if int(recurso)>Elixir:
                    recursosfaltantes=int(recurso)-Elixir
                    tiempoextra=recursosfaltantes/porsec
                    tiemp+=int(tiempoextra)+1
                    Elixir=0
                    boole=True
                #si se tiene suficiente recurso se debe usar
                else:
                    Elixir-=int(recurso)
        #si se debe usar oro
        else:
            #obtener la cantidad de recurso que se debe usar
            recurso=resourcesOr[jobs.columns[operacion]].values[key_count[operacion]]
            if(recurso!='None'):
                #si no se tiene suficiente recurso se debe esperar a que se obtenga
                if int(recurso)>Oro:
                    recursosfaltantes=int(recurso)-Oro
                    tiempoextra=recursosfaltantes/porsec
                    tiemp+=int(tiempoextra)+1
                    Oro=0
                    boole=True
                #si se tiene suficiente recurso se debe usar
                else:
                    Oro-=int(recurso)
        #se debe sumar el tiempo de la operacion a la maquina y al trabajo
        maquinas[maquina]+=int(tiemp)
        trabajos[operacion]+=int(tiemp)
        #se debe actualizar el tiempo de la maquina y del trabajo para que vayan en paralelo
        if(maquinas[maquina]>trabajos[operacion]):
            trabajos[operacion]=maquinas[maquina]
        else:
            maquinas[maquina]=trabajos[operacion]
        key_count[operacion]+=1
    return max(trabajos)


#operador de movimiento para el algoritmo de busqueda local hill climbing
def operadormovimiento(solucion):
    combinaciones = []
    #intercambio de dos elementos, se genera una permutacion
    for i in range(len(solucion)):
        for j in range(len(solucion)):
            if i != j:
                permutacion=solucion.copy()
                permutacion[i],permutacion[j]=permutacion[j],permutacion[i] 
                combinaciones.append(permutacion)
    #entrega todas las combinaciones posibles de intercambiar 2 elementos n cuadrado
    return combinaciones

#algoritmo de busqueda local local hill climbing
def hill_climbing(solucion_inicial,tiempos,recursosEl,recursosOro,storageE,storageO,reg):
    makespan_record=[]
    optimo=9999999999999999999999
    solucion=solucion_inicial
    iteraciones=0
    while True:
        print("Siguiente Iteración")
        mejor_vecino=None
        for vecino in operadormovimiento(solucion):#generar vecinos de la solucion
            valor=evaluate_solution(tiempos,recursosEl,recursosOro,vecino,storageE,storageO,reg)#evaluar la solucion
            if valor<optimo:#si la solucion es mejor se actualiza
                print("Se mejoró un: ",(optimo-valor)/optimo*100,"%")
                print("\t",optimo,"->",valor,"\n")
                optimo=valor
                makespan_record.append(optimo)
                mejor_vecino=vecino
        if mejor_vecino!=None:
            solucion=mejor_vecino
        else:
            break
    return solucion,makespan_record

#Generar una solucion inicial segun la cantidad de trabajos con sus niveles respectivos
def solucion_init(jobs):
    solucion=[]
    contador=0
    for i in jobs.columns:
        for j in jobs[i]:
            if j!="None":
                solucion.append(contador)
        contador+=1
    random.shuffle(solucion)#desordenar la solucion
    return solucion

def main():
    #leer los datos de los trabajos
    ayuntamiento=input("Introduce el ayuntamiento:")
    tiempos=pd.read_csv(f'./test/{ayuntamiento}_time.csv',sep=',',index_col=0)
    recursosOro=pd.read_csv(f'./test/{ayuntamiento}_gold.csv',sep=',',index_col=0)
    recursosEl=pd.read_csv(f'./test/{ayuntamiento}_elixir.csv',sep=',',index_col=0)
    capacidad=pd.read_csv(f'./available/storage_and_regen.csv',sep=',',index_col=0)
    storageE=capacidad['Storage'].values[int(ayuntamiento)-1]
    storageG=capacidad['Storage'].values[int(ayuntamiento)-1]
    reg=capacidad['Regen'].values[int(ayuntamiento)-1]
    solucion=solucion_init(tiempos)
    start = time.time()
    solucion,recods=hill_climbing(solucion,tiempos,recursosEl,recursosOro,storageE,storageG,reg)
    end = time.time()
    print("tiempo de ejecucion:",end - start,"segundos",'\tAyuntamiento:',ayuntamiento)
    df=grafico(tiempos,recursosEl,recursosOro,solucion,storageE,storageG,reg)
    #graficar el resultado
    colors = {i: f'rgb({random.randint(0,255)},{random.randint(0,255)}, {random.randint(0,255)})' for i in tiempos.columns}

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                        group_tasks=True)
    fig.show()
    plt.plot([i for i in range(len(recods))],recods,'b')
    plt.ylabel('Makespan',fontsize=15)
    plt.xlabel('Soluciones',fontsize=15)
    plt.show()
if __name__ == '__main__':
    main()


