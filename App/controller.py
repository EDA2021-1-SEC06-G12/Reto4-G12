"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import stack as st
from DISClib.Algorithms.Sorting import mergesort as mrge
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf
import tracemalloc
import time

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def cargar(analyzer):
    
    landingpointsfile = cf.data_dir + "landing_points.csv"
    input_file = csv.DictReader(open(landingpointsfile, encoding="utf-8"),
                                delimiter=",")
    for point in input_file:
        model.addLandingPoint(analyzer,point)


    connectionsfile = cf.data_dir + "connections.csv"
    input_file = csv.DictReader(open(connectionsfile, encoding="utf-8"),delimiter=",")
    for connection in input_file:
        model.addLP_cable(analyzer, connection)
 
    countriesfile = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(countriesfile, encoding="utf-8"),
                                delimiter=",")
    for country in input_file:
        model.addCountry(analyzer,country)

    countriesfile2 = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(countriesfile2, encoding="utf-8"),
                                delimiter=",")
    for country2 in input_file:
        model.addCapital_V_E(analyzer,country2)
    
    model.edges_same_lp(analyzer)
    
  
    
    num_lps = mp.size(analyzer["landing_points"])
    num_conexiones = gr.numEdges(analyzer["connections_distance"])
    num_paises = mp.size(analyzer["countries"])

  
    return num_lps,num_conexiones,num_paises
    
# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def req1(analyzer,lp1,lp2):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    num1=model.iddadolp(analyzer,lp1)
    num2=model.iddadolp(analyzer,lp2)
    if num1==None or num2==None:

        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)

        return None
        
    else:
        x=model.req1(analyzer,num1,num2)

        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)

        return x

def req2(analyzer):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    lista = model.req2(analyzer)  
    lista_sorteada = lt.subList(mrge.sort(lista, cmpreq2), 1, 1)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return lista_sorteada
        
def req3(analyzer,pais1,pais2):

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    capital1=model.capital(analyzer,pais1.lower())
    capital2=model.capital(analyzer,pais2.lower())
    if capital1==None or capital2==None:
        print('No hay información para los países dados.')
    else:
        distpath=model.distpath(analyzer,capital1,capital2)
        distancia=distpath[0]
        path = distpath[1]
        
        print('La distancia total de la ruta es de: '+str(distancia)+' km.')
        print("")
        print('\nLa ruta está dada por: ')
        
        i = 1
        inicial = st.size(path)
        while i<=inicial:
            sub = st.pop(path)
            if i == 1:
                vertexA = sub["vertexA"][0] + str(" " + str(pais1))
                cableA = "CAPITAL"
            else:
                place = mp.get(analyzer["name_dado_id"], sub["vertexA"][0])
                if place != None:
                    vertexA = place["value"]
                    cableA = str(sub["vertexA"][1])
                else:
                    vertexA = sub["vertexA"][0] 
                    cableA = "CAPITAL"
            
            place = mp.get(analyzer["name_dado_id"], sub["vertexB"][0])
            if place != None:
                vertexB = place["value"]
                cableB = str(sub["vertexB"][1])
            else:
                vertexB = sub["vertexB"][0].upper() 
                cableB = "CAPITAL"

            print("---------------------")
            print(str(i) + ") ACTUAL: " + str(vertexA) +" |CABLE: "+ cableA  + " -> SIGUIENTE: " + str(vertexB) +" |CABLE: "+ cableB + str(" | DISTANCIA (KM): ") +str(sub["weight"]))
            i += 1
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        
        return None
           
def req4(analyzer):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    x = model.req4(analyzer)
    num_nodos = x[0]
    costo = x[1]
    camino = x[2]
    print("El número de nodos conectados a la red de expansión mínima es: " + str(num_nodos))
    print("El costo total (distancia en [km]) de la red de expansión mínima es: " + str(costo))
    print("Rama más larga: ")
    print(camino)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return None

def req5(analyzer,lp_name):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    id = mp.get(analyzer["id_dado_lp"], lp_name)["value"]
    mapa = model.req5(analyzer,id)
    paises = mp.keySet(mapa)
    final = lt.newList(datastructure="ARRAY_LIST")
    i=1
    while i <= lt.size(paises):
        pais = lt.getElement(paises, i)
        distancia = mp.get(mapa, pais)["value"]
        lt.addLast(final, (pais,distancia))
        i+=1
    mrge.sort(final, cmpaux2)

    ii = 1
    while ii <= lt.size(final):
        elemento = lt.getElement(final, ii)
        print("PAIS: " + str(elemento[0]) + " | DISTANCIA (KM): " + str(elemento[1]))
        ii+=1
    print(str(lt.size(final)) + " paises afectados")

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return None

def req6(analyzer,pais,cable):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    mapa = model.req6(analyzer,pais,cable)
    lista = mp.keySet(mapa)
    i = 1
    while i <= lt.size(lista):
        pais = lt.getElement(lista, i)
        ancho_banda = mp.get(mapa, pais)["value"]
        print("PAIS: " + str(pais) + " ANCHO DE BANDA MAX (MBPS): " + str(ancho_banda))
        i+=1
    
    if lt.size(lista) == 0:
        print("Ningún pais además de " + str(pais).upper() + " fue afectado")
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return None

def cmpaux(tupla1,tupla2):
    return(float(tupla1[0])>=float(tupla2[0]))

def cmpaux2(tupla1,tupla2):
    return(float(tupla1[1])>=float(tupla2[1]))

def cmpreq2(tupla1,tupla2):
    return(float(tupla1[1])>=float(tupla2[1]))









def getTime():
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory