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
    """
    print(gr.numVertices(analyzer["connections_distance"]))

    lista = mp.keySet(analyzer["vertices"])
    i = 1
    suma = 0
    while i <= lt.size(lista):
        lista2 = mp.get(analyzer["vertices"], lt.getElement(lista, i))["value"]
        ii = 1
        lista3 = lt.newList()
        while ii <= lt.size(lista2):
            elem = lt.getElement(lista2, ii)["LP_cable"]
            lt.addLast(lista3, elem)
            ii += 1
        print(lista3)
        print("")
        
        suma += lt.size(lista2)
        i+=1
    
    print(suma)
"""
    """
    lista = gr.vertices(analyzer["connections_distance"])
    i = 1
    final = lt.newList(datastructure="ARRAY_LIST")
    while i <= lt.size(lista):
        vertice = lt.getElement(lista, i)

        lt.addLast(final, vertice)
        i+=1
    mrge.sort(final,cmpaux)
    print(final)
    print("")
    print(mp.size(analyzer["vertices_aux"]))
    print("")
    """
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
    
    """
    num_lps = gr.numVertices(analyzer["connections_distance"])
    num_conexiones = gr.numEdges(analyzer["connections_distance"])
    num_paises = mp.size(analyzer["countries"])
"""
    
    num_lps = mp.size(analyzer["landing_points"])
    num_conexiones = gr.numEdges(analyzer["connections_distance"])
    num_paises = mp.size(analyzer["countries"])

    """
    print(lt.subList(gr.vertices(analyzer["connections_distance"]), 1, 20))
    print(mp.get(analyzer["name_dado_id"], "4862")["value"])
    print(gr.adjacents(analyzer["connections_distance"], ('4862', 'Dunant')))
    """
    return num_lps,num_conexiones,num_paises
    
# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def req1(analyzer,lp1,lp2):
    num1=model.iddadolp(analyzer,lp1)
    num2=model.iddadolp(analyzer,lp2)
    if num1==None or num2==None:
        return None
    else:
        x=model.req1(analyzer,num1,num2)
        return x

def req2(analyzer):
    lista = model.req2(analyzer)  
    lista_sorteada = lt.subList(mrge.sort(lista, cmpreq2), 1, 1)
    return lista_sorteada
        
def req3(analyzer,pais1,pais2):
    capital1=model.capital(analyzer,pais1.lower())
    capital2=model.capital(analyzer,pais2.lower())
    if capital1==None or capital2==None:
        print('No hay información para los países dados.')
    else:
        distpath=model.distpath(analyzer,capital1,capital2)
        distancia=distpath[0]
        path = distpath[1]
        print(path)
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
        
        return distancia
           
def req4(analyzer):
    x = model.req4(analyzer)
    num_nodos = x[0]
    costo = x[1]
    camino = x[2]
    print("El número de nodos conectados a la red de expansión mínima es: " + str(num_nodos))
    print("El costo total (distancia en [km]) de la red de expansión mínima es: " + str(costo))
    print("Rama más larga: ")
    print(camino)

def req5(analyzer,lp_name):
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

def req6(analyzer,pais,cable):
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

def cmpaux(tupla1,tupla2):
    return(float(tupla1[0])>=float(tupla2[0]))

def cmpaux2(tupla1,tupla2):
    return(float(tupla1[1])>=float(tupla2[1]))

def cmpreq2(tupla1,tupla2):
    return(float(tupla1[1])>=float(tupla2[1]))