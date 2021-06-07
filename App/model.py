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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import haversine as hs
from DISClib.ADT import stack as st
from DISClib.DataStructures import arraylistiterator as it
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Sorting import mergesort as mrge
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

# Funciones para agregar informacion al catalogo

def newAnalyzer():
  
    try:
        analyzer = {
                    'countries': None,
                    "landing_points":None,
                    'connections_distance': None,
                    'connections_capacity': None,
                    'components': None,
                    'id_dado_lp': None,
                    'paths': None,
                    "identificadores":None
                    }

        analyzer['countries'] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer["country_dado_city"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer['landing_points_country'] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')
        
        analyzer["id_dado_lp"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer["location_dado_id"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')
       
        analyzer["name_dado_id"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer["landing_points"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer["cables_dado_lpid"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')
        
        analyzer['vertices'] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')
        
        analyzer['vertices_aux'] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer["edges"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')


        analyzer['connections_distance'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True, size=5000,
                                               comparefunction=None)

        
        analyzer['connections_capacity'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,size=5000,
                                                comparefunction=None)
        
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo
def addCountry(analyzer,country):
    mp.put(analyzer["countries"],country["CountryName"].lower(),country)
    mp.put(analyzer["country_dado_city"],country["CapitalName"].lower(),country["CountryName"].lower())

def addLandingPoint(analyzer,point):
    mp.put(analyzer["landing_points"],point["landing_point_id"],point)

    cityandcountry = point["name"]
    lista=(cityandcountry.lower()).split(', ')
    if len(lista) > 2:
        city = lista[0] + ", " + lista[1]
        country = lista[2]
        mp.put(analyzer["landing_points_country"],str(point["landing_point_id"]),country)
        mp.put(analyzer["id_dado_lp"],cityandcountry.lower(), str(point["landing_point_id"]))
        mp.put(analyzer["location_dado_id"],str(point["landing_point_id"]),(float(point["latitude"]),float(point["longitude"])))
        mp.put(analyzer["name_dado_id"], str(point["landing_point_id"]), cityandcountry)

    elif len(lista) > 1:
        city = lista[0]
        country = lista[1]
        mp.put(analyzer["landing_points_country"],str(point["landing_point_id"]),country)
        mp.put(analyzer["id_dado_lp"],cityandcountry.lower(), str(point["landing_point_id"]))
        mp.put(analyzer["location_dado_id"],str(point["landing_point_id"]),(float(point["latitude"]),float(point["longitude"])))
        mp.put(analyzer["name_dado_id"], str(point["landing_point_id"]), cityandcountry)
    else:
        mp.put(analyzer["landing_points_country"],str(point["landing_point_id"]),lista[0])
        mp.put(analyzer["id_dado_lp"],cityandcountry.lower(), str(point["landing_point_id"]))
        mp.put(analyzer["location_dado_id"],str(point["landing_point_id"]),(float(point["latitude"]),float(point["longitude"])))
        mp.put(analyzer["name_dado_id"], str(point["landing_point_id"]), cityandcountry)

    

def addLP_cable(analyzer,element):
    graph_distance = analyzer["connections_distance"]
    graph_capacity = analyzer["connections_capacity"]
  
    id_origin = str(element["\ufefforigin"])
    country_origin = mp.get(analyzer["landing_points_country"], id_origin)["value"]

    LP_cable_origin = (str(element["\ufefforigin"]),str(element["cable_name"]))
    if mp.contains(analyzer["vertices"], country_origin):
        mapa_aux = mp.get(analyzer["vertices"], country_origin)["value"]
        mp.put(mapa_aux,LP_cable_origin,element)
    else:
        mapa_aux = mp.newMap()
        mp.put(analyzer["vertices"],country_origin,mapa_aux)
        mp.put(mapa_aux, LP_cable_origin, element)
    
    if mp.contains(analyzer["cables_dado_lpid"], LP_cable_origin[0]):
        mapa_aux = mp.get(analyzer["cables_dado_lpid"], LP_cable_origin[0])["value"]
        mp.put(mapa_aux,LP_cable_origin[1],None)
    else:
        mapa_aux = mp.newMap()
        mp.put(analyzer["cables_dado_lpid"],LP_cable_origin[0],mapa_aux)
        mp.put(mapa_aux, LP_cable_origin[1], None)

    id_destination = str(element["destination"])
    country_destination = mp.get(analyzer["landing_points_country"], id_destination)["value"]
    
    LP_cable_destination = (str(element["destination"]),str(element["cable_name"]))
    if mp.contains(analyzer["vertices"], country_destination):
        mapa_aux = mp.get(analyzer["vertices"], country_destination)["value"]
        mp.put(mapa_aux,LP_cable_destination,element)
    else:
        mapa_aux = mp.newMap()
        mp.put(analyzer["vertices"],country_destination,mapa_aux)
        mp.put(mapa_aux, LP_cable_destination, element)
    
    if mp.contains(analyzer["cables_dado_lpid"], LP_cable_destination[0]):
        mapa_aux = mp.get(analyzer["cables_dado_lpid"], LP_cable_destination[0])["value"]
        mp.put(mapa_aux,LP_cable_destination[1],None)
    else:
        mapa_aux = mp.newMap()
        mp.put(analyzer["cables_dado_lpid"],LP_cable_destination[0],mapa_aux)
        mp.put(mapa_aux, LP_cable_destination[1], None)

    if not gr.containsVertex(graph_distance, LP_cable_origin) and not mp.contains(analyzer["vertices_aux"], LP_cable_origin):
        gr.insertVertex(graph_distance, LP_cable_origin)
    
    if not gr.containsVertex(graph_distance, LP_cable_destination)and not mp.contains(analyzer["vertices_aux"], LP_cable_destination):
        gr.insertVertex(graph_distance, LP_cable_destination)
    
    if not gr.containsVertex(graph_capacity, LP_cable_origin) and not mp.contains(analyzer["vertices_aux"], LP_cable_origin):
        gr.insertVertex(graph_capacity, LP_cable_origin)
    
    if not gr.containsVertex(graph_capacity, LP_cable_destination)and not mp.contains(analyzer["vertices_aux"], LP_cable_destination):
        gr.insertVertex(graph_capacity, LP_cable_destination)

    mp.put(analyzer["vertices_aux"],LP_cable_destination,None)
    mp.put(analyzer["vertices_aux"],LP_cable_origin,None)

    addLP_cable_Edges(analyzer,LP_cable_origin,LP_cable_destination,element)

def addLP_cable_Edges(analyzer,origin,destination,element):
    graph_distance = analyzer["connections_distance"]
    graph_capacity = analyzer["connections_capacity"]

    splitted = element["cable_length"].split(" ", 1)
    if splitted[0] != "n.a.":
        distance = float(splitted[0].replace(",",""))
    else:
        distance = 500
    
    cost = {"distance":distance,"capacity":float(element["capacityTBPS"])}

    edge_identifier = (origin,destination)
    mp.put(analyzer["edges"],edge_identifier,cost)
    gr.addEdge(graph_distance, origin, destination, cost["distance"])
    gr.addEdge(graph_capacity, origin, destination, cost["capacity"])


def addCapital_V_E(analyzer,element):
    
    graph_distance = analyzer["connections_distance"]
    graph_capacity = analyzer["connections_capacity"]

    country = element["CountryName"].lower()
    city = element["CapitalName"].lower()
    
    if not gr.containsVertex(graph_distance,(city,0)):
        gr.insertVertex(graph_distance,(city,0))
    
    if not gr.containsVertex(graph_capacity,(city,0)):
        gr.insertVertex(graph_capacity,(city,0))

    if mp.get(analyzer["vertices"],country) != None:
        mapa = mp.get(analyzer["vertices"],country)["value"]
        lista = mp.keySet(mapa)
        i=1
        while i <= lt.size(lista):
            lp_cable=lt.getElement(lista, i)

            info_lp_cable = mp.get(mapa, lp_cable)["value"]
            tuple_place_cablename = lp_cable
            id_place = tuple_place_cablename[0]
            location = mp.get(analyzer["location_dado_id"],id_place)["value"]
            edge_identifier = (tuple_place_cablename,(city,0))

            cost = {"distance":None,"capacity":None}
            cost["distance"] = float(hs.haversine(location,(float(element["CapitalLatitude"]),float(element["CapitalLongitude"]))))
            cost["capacity"] = float(info_lp_cable["capacityTBPS"])
        
            mp.put(analyzer["edges"],edge_identifier,cost)

            gr.addEdge(graph_distance, tuple_place_cablename, (city,0), cost["distance"])
            gr.addEdge(graph_distance, (city,0), tuple_place_cablename, cost["distance"])

            gr.addEdge(graph_capacity, tuple_place_cablename, (city,0), cost["capacity"])
            gr.addEdge(graph_capacity, (city,0), tuple_place_cablename, cost["capacity"])

            i+=1
    else:
        sinMar(analyzer,country,city)

    

   
def sinMar(analyzer,country,city):
    info = mp.get(analyzer["countries"], country)["value"]
    location = (float(info["CapitalLatitude"]),float(info["CapitalLongitude"]))
    lista3 = mp.keySet(analyzer["vertices"])

    lista_final = lt.newList(datastructure="ARRAY_LIST")
    i=1
    while i<=lt.size(lista3):
        country=lt.getElement(lista3, i)
        mapa = mp.get(analyzer["vertices"],country)["value"]
        lista2 = mp.keySet(mapa)
        ii = 1
        while ii<=lt.size(lista2):
            lp_name = lt.getElement(lista2, ii)
            lp = mp.get(mapa, lp_name)["value"]
            location_lp = mp.get(analyzer["location_dado_id"], lp_name[0])["value"]
            capacity = float(lp["capacityTBPS"])
            distance = hs.haversine(location_lp, location)
            lt.addLast(lista_final, (lp_name,distance,capacity))
            ii += 1
        i+=1
        
    lista_sorteada = mrge.sort(lista_final,cmpSinMar)
    tupla = lt.getElement(lista_sorteada, 1)
    cost = {"distance":tupla[1],"capacity":float(tupla[2])}
    edge_identifier = (tupla[0],(city,0))
    mp.put(analyzer["edges"],edge_identifier,cost)

    gr.addEdge(analyzer["connections_distance"], tupla[0], (city,0), cost["distance"])
    gr.addEdge(analyzer["connections_distance"], (city,0), tupla[0], cost["distance"])

    gr.addEdge(analyzer["connections_capacity"], tupla[0], (city,0), cost["capacity"])
    gr.addEdge(analyzer["connections_capacity"], (city,0), tupla[0], cost["capacity"])

def edges_same_lp(analyzer):
    lista = mp.keySet(analyzer["vertices"])
    mapa_landingpoints = mp.newMap()
    i = 1
    while i<=lt.size(lista):
        country = lt.getElement(lista, i)
        mapa = mp.get(analyzer["vertices"],country)["value"]
        lista2 = mp.keySet(mapa)
        ii = 1
        while ii<=lt.size(lista2):
            lp1 = lt.getElement(lista2, ii)
            lp1_all = entryvert(lp1, mp.get(mapa, lp1)["value"])
            lp1_name = lp1
            lp1_place = lp1_name[0]
            if mp.contains(mapa_landingpoints, lp1_place):
                listaaux = mp.get(mapa_landingpoints, lp1_place)["value"]
                lt.addLast(listaaux,lp1_all)
            else:
                listaaux = lt.newList(datastructure="ARRAY_LIST")
                mp.put(mapa_landingpoints,lp1_place,listaaux)
                lt.addLast(listaaux,lp1_all)
            ii += 1
        i +=1
    
    add_edges_same_lp(analyzer,mapa_landingpoints)

def add_edges_same_lp(analyzer,mapa):
    lista = mp.keySet(mapa)

    i = 1
    while i<=lt.size(lista):
        lp = lt.getElement(lista, i)
        lista_vertices = mp.get(mapa, lp)["value"]

        ii = 1
        while ii<=lt.size(lista_vertices):
            lp1 = lt.getElement(lista_vertices, ii)
            lp1_name = lp1["LP_cable"]
            
            e = ii+1
            while e<=lt.size(lista_vertices):
                lp2 = lt.getElement(lista_vertices, e)
                lp2_name = lp2["LP_cable"]
                cost = {"distance":None,"capacity":None}
                cost["distance"] = float(0.1)
                cost["capacity"] = min(float(lp1["info"]["capacityTBPS"]),float(lp2["info"]["capacityTBPS"]))
                mp.put(analyzer["edges"],(lp1_name,lp2_name),cost)
                gr.addEdge(analyzer["connections_distance"], lp1_name, lp2_name, cost["distance"])
                gr.addEdge(analyzer["connections_distance"], lp2_name, lp1_name, cost["distance"])

                gr.addEdge(analyzer["connections_capacity"], lp1_name, lp2_name, cost["capacity"])
                gr.addEdge(analyzer["connections_capacity"], lp2_name, lp1_name, cost["capacity"])
                e +=1

            ii += 1   

        i+=1
            





def entryvert(Lp_cable, element):
    entry={'LP_cable':Lp_cable,'info':element}
    return entry
    

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compareLPs(LP1, LP2):
    """
    Compara dos estaciones
    """
    LP2 = LP2["key"]
    if (LP1 == LP2):
        return 0
    elif (LP1 > LP2):
        return 1
    else:
        return -1

def cmpSinMar(tupla1,tupla2):
    return(float(tupla1[1])<=float(tupla2[1]))

##Requerimientos

def req1(analyzer,lpId_1,lpId_2):
    try:
        estructura_kosaraju = scc.KosarajuSCC(analyzer["connections_distance"])
        num_clusteres = scc.connectedComponents(estructura_kosaraju)
    
        cable_1 = lt.getElement(mp.keySet(mp.get(analyzer["cables_dado_lpid"], lpId_1)["value"]),1)
        cable_2 = lt.getElement(mp.keySet(mp.get(analyzer["cables_dado_lpid"], lpId_2)["value"]),1)
        
        valor = scc.stronglyConnected(estructura_kosaraju,(lpId_1,cable_1),(lpId_2,cable_2))
        
        return num_clusteres,valor

    except:
        estructura_kosaraju = scc.KosarajuSCC(analyzer["connections_distance"])
        num_clusteres = scc.connectedComponents(estructura_kosaraju)

        return num_clusteres,True

def iddadolp(analyzer,lp):
    ide=(mp.get(analyzer['id_dado_lp'],lp))
    if ide!=None:
        return ide['value']
    else:
        return None

def req2(analyzer):
    lista_vertices = gr.vertices(analyzer["connections_distance"])
    final = lt.newList(datastructure="ARRAY_LIST")
    i = 1
    while i <=lt.size(lista_vertices):
        elem = lt.getElement(lista_vertices, i)
        if gr.degree(analyzer["connections_distance"], elem)>1 and elem[1] != 0:
            lp_id = elem[0]
            lp_name = mp.get(analyzer["name_dado_id"], lp_id)["value"]
            lista_adyacentes = gr.adjacents(analyzer["connections_distance"], elem)

            ii = 1
            e = 0
            while ii <= lt.size(lista_adyacentes):
                adyacente = lt.getElement(lista_adyacentes, ii)
                if adyacente[0] == lp_id:
                    e += 1
                ii+=1
            if e >= 1:
                lt.addLast(final, (lp_name,e+1))
        i+=1
    return final



def capital(analyzer,pais):
    mapa=analyzer['countries']
    par=(mp.get(mapa,pais))
    if par==None:
        return None
    else:
        element=me.getValue(par)
        capital=element['CapitalName'].lower()
        return capital

def distpath(analyzer,capital1,capital2):
    camino=lt.newList()
    estructura=djk.Dijkstra(analyzer['connections_distance'],(capital1,0))
    distancia=djk.distTo(estructura,(capital2,0))
    path=djk.pathTo(estructura,(capital2,0))
    return distancia,path

def req4(analyzer):
    estructura = pr.PrimMST(analyzer["connections_distance"])
    costo_total = pr.weightMST(analyzer["connections_distance"], estructura)

    grafo_mst = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True, size=5000,
                                               comparefunction=None)
    i = 1
    while i<= lt.size(estructura["mst"]):
        arista = lt.getElement(estructura["mst"], i)
        verticeA = arista["vertexA"]
        verticeB = arista["vertexB"]
        weight = arista["weight"]

        if not gr.containsVertex(grafo_mst, verticeA):
            gr.insertVertex(grafo_mst, verticeA)

        if not gr.containsVertex(grafo_mst, verticeB):
            gr.insertVertex(grafo_mst, verticeB)
        
        gr.addEdge(grafo_mst, verticeA, verticeB, weight)
        gr.addEdge(grafo_mst, verticeB, verticeA, weight)

        i += 1

    num_vertices = gr.numVertices(grafo_mst)

    vertices_mst = gr.vertices(grafo_mst)

    inicio = lt.firstElement(estructura["mst"])["vertexA"]
   
    final = lt.lastElement(estructura["mst"])["vertexB"]

    estructura_dfs = dfs.DepthFirstSearch(grafo_mst, inicio)
    caminoo = dfs.pathTo(estructura_dfs, final)
    
    
    return num_vertices, costo_total,caminoo
    
    


def req5(analyzer,id):
    lista_vertices = gr.vertices(analyzer["connections_distance"])
    lista_vertices_lp = lt.newList(datastructure="ARRAY_LIST")
    i = 1
    while i<= lt.size(lista_vertices):
        vertice = lt.getElement(lista_vertices, i)
        if vertice[0] == id: 
            lt.addLast(lista_vertices_lp, vertice)
        i += 1
    paises_afectados = mp.newMap()
    ii = 1
    while ii <= lt.size(lista_vertices_lp):
        vertice = lt.getElement(lista_vertices_lp, ii)
        adyacentes = gr.adjacents(analyzer["connections_distance"], vertice)
        iii = 1
        while iii <= lt.size(adyacentes):
            adyacente = lt.getElement(adyacentes, iii)
            if adyacente[1] == 0:
                pais_afectado = mp.get(analyzer["country_dado_city"], adyacente[0])["value"]
                distancia = gr.getEdge(analyzer["connections_distance"], vertice, adyacente)["weight"]

            else:
                id_adyacente = adyacente[0]
                pais_afectado = mp.get(analyzer["landing_points_country"], id_adyacente)["value"]
                distancia = gr.getEdge(analyzer["connections_distance"], vertice, adyacente)["weight"]
            
            if mp.contains(paises_afectados,pais_afectado):
                valor_ant = mp.get(paises_afectados, pais_afectado)["value"]
                if distancia < valor_ant:
                    mp.put(paises_afectados, pais_afectado, distancia)
            else:
                mp.put(paises_afectados, pais_afectado,distancia)
            
            iii += 1

        ii += 1
        
    return paises_afectados

def req6(analyzer,pais,cable):

    vertices = gr.vertices(analyzer["connections_capacity"])
    ciudad_cap = mp.get(analyzer["countries"], pais)["value"]["CapitalName"].lower()
    vertice_ciudad = (ciudad_cap,0)
    adyacentes_ciudad_cable = adyacentes_ciudad_cabl(analyzer,vertice_ciudad,cable)

    mapa_adyacentestotales = mp.newMap()
    i = 1
    while i <= lt.size(vertices):
        vertice = lt.getElement(vertices, i)
        if vertice[1] == cable:
            
            pais_adyacente2 = mp.get(analyzer["landing_points_country"],vertice[0])["value"]
            
            poblacion = float(mp.get(analyzer["countries"], pais_adyacente2)["value"]["Population"].replace(".",""))

            ii = 1
            while ii <= lt.size(gr.adjacents(analyzer["connections_capacity"],vertice)):
                inicio2 = lt.getElement(gr.adjacents(analyzer["connections_capacity"],vertice),ii)
                if inicio2[1] == cable:
                    inicio = inicio2
                    break
                ii +=1 

            capacity_mbps = float(gr.getEdge(analyzer["connections_capacity"], inicio, vertice)["weight"])*1000000
            valor = capacity_mbps/poblacion
           
            if pais_adyacente2 != pais:
                if mp.contains(mapa_adyacentestotales, pais_adyacente2):
                    valor_ant = mp.get(mapa_adyacentestotales, pais_adyacente2)["value"]
                    if valor_ant < valor:
                        mp.put(mapa_adyacentestotales, pais_adyacente2, valor)
                else:
                    mp.put(mapa_adyacentestotales, pais_adyacente2, valor)
        i+=1

    
    return mapa_adyacentestotales
    
def adyacentes_ciudad_cabl(analyzer,vertice_ciudad,cable):
    lista_adyacentes = gr.adjacents(analyzer["connections_capacity"], vertice_ciudad)
    lista_adyacentes_cable = lt.newList(datastructure="ARRAY_LIST")

    i = 1
    while i <= lt.size(lista_adyacentes):
        adyacente = lt.getElement(lista_adyacentes, i)
        if adyacente[1] == cable:
            lt.addLast(lista_adyacentes_cable, adyacente)
        i+=1
    return lista_adyacentes_cable

def caminos(analyzer,adyacentes_ciudad_cable):
    lista_caminos = lt.newList(datastructure="ARRAY_LIST")
    vertices = gr.vertices(analyzer["connections_capacity"])

    i = 1
    while i <= lt.size(adyacentes_ciudad_cable):
        adyacente = lt.getElement(adyacentes_ciudad_cable,i)
        dfs_adyacente = dfs.DepthFirstSearch(analyzer["connections_capacity"], adyacente)

        ii = 1
        while ii <= lt.size(vertices):
            vertice = lt.getElement(vertices, ii)
            if vertice[1] == cable:
                verdad = dfs.hasPathTo(dfs_adyacente, vertice)
                camino = dfs.pathTo(dfs_adyacente, vertice)
                lt.addLast(lista_caminos,camino)
            ii += 1
        
        i+=1
    
    return lista_caminos