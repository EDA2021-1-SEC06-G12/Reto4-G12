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
from DISClib.DataStructures import arraylistiterator as it
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Sorting import mergesort as mrge
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

# Funciones para agregar informacion al catalogo

def newAnalyzer():
    """ Inicializa el analizador
   countries: Tabla de hash para guardar los paises
   landing_points: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre landing_points
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'countries': None,
                    "landing_points":None,
                    'connections': None,
                    'components': None,
                    'id_dado_lp': None,
                    'paths': None,
                    "identificadores":None
                    }

        analyzer['countries'] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer['landing_points_country'] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')
        
        analyzer["id_dado_lp"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer["location_dado_id"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')
        
        analyzer['vertices'] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')

        analyzer["edges"] = mp.newMap(loadfactor=0.5,
                                     maptype='PROBING')


        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000, comparefunction=compareLPs)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo



def addLandingPoint(analyzer,point):
    cityandcountry = point["name"]
    lista=(cityandcountry.lower()).split(', ')
    if len(lista) > 1:
        city = lista[0]
        country = lista[1]
        mp.put(analyzer["landing_points_country"],str(point["landing_point_id"]),country)
        mp.put(analyzer["id_dado_lp"],city, str(point["landing_point_id"]))
        mp.put(analyzer["location_dado_id"],str(point["landing_point_id"]),(float(point["latitude"]),float(point["longitude"])))
    else:
        mp.put(analyzer["landing_points_country"],str(point["landing_point_id"]),lista[0])
        mp.put(analyzer["id_dado_lp"],lista[0], str(point["landing_point_id"]))
        mp.put(analyzer["location_dado_id"],str(point["landing_point_id"]),(float(point["latitude"]),float(point["longitude"])))

    

def addLP_cable(analyzer,element):
    graph = analyzer["connections"]
  
    id_origin = str(element["\ufefforigin"])
    country_origin = mp.get(analyzer["landing_points_country"], id_origin)["value"]

    LP_cable_origin = (str(element["\ufefforigin"]),str(element["cable_name"]))
    if mp.contains(analyzer["vertices"], country_origin):
        lista = mp.get(analyzer["vertices"], country_origin)["value"]
        entry = entryvert(LP_cable_origin,element)
        lt.addLast(lista,entry)
    else:
        lista = lt.newList(datastructure="ARRAY_LIST")
        mp.put(analyzer["vertices"],country_origin,lista)
        entry = entryvert(LP_cable_origin,element)
        lt.addLast(lista, entry)

    id_destination = str(element["destination"])
    country_destination = mp.get(analyzer["landing_points_country"], id_destination)["value"]
    
    LP_cable_destination = (str(element["destination"]),str(element["cable_name"]))
    if mp.contains(analyzer["vertices"], country_destination):
        lista = mp.get(analyzer["vertices"], country_destination)["value"]
        entry = entryvert(LP_cable_destination,element)
        lt.addLast(lista,entry)
    else:
        lista = lt.newList(datastructure="ARRAY_LIST")
        mp.put(analyzer["vertices"],country_destination,lista)
        entry = entryvert(LP_cable_destination,element)
        lt.addLast(lista, entry)

    if not gr.containsVertex(graph, LP_cable_origin):
        gr.insertVertex(graph, LP_cable_origin)
    
    if not gr.containsVertex(graph, LP_cable_destination):
        gr.insertVertex(graph, LP_cable_destination)
    
    addLP_cable_Edges(analyzer,LP_cable_origin,LP_cable_destination,element)

def addLP_cable_Edges(analyzer,origin,destination,element):
    graph = analyzer["connections"]
    splitted = element["cable_length"].split(" ", 1)
    if splitted[0] != "n.a.":
        distance = float(splitted[0].replace(",",""))
    else:
        distance = 100000000000000000000000000000000
    
    cost = {"distance":distance,"capacity":float(element["capacityTBPS"])}

    edge_identifier = (origin,destination)
    mp.put(analyzer["edges"],edge_identifier,cost)
    gr.addEdge(graph, origin, destination, cost)

def addCapital_V_E(analyzer,element):
    
    graph = analyzer["connections"]
    country = element["CountryName"].lower()
    city = element["CapitalName"].lower()
    
    
    mp.put(analyzer["countries"], country,element)

    if not gr.containsVertex(graph,(city,0)):
        gr.insertVertex(graph,(city,0))

    if mp.get(analyzer["vertices"],country) != None:
        lista = mp.get(analyzer["vertices"],country)["value"]
        i=it.newIterator(lista)
        while it.hasNext(i):
            lp_cable=(it.next(i))

            info_lp_cable = lp_cable["info"]
            tuple_place_cablename = lp_cable["LP_cable"]
            id_place = tuple_place_cablename[0]
            location = mp.get(analyzer["location_dado_id"],id_place)["value"]
            edge_identifier = (lp_cable["LP_cable"],(city,0))

            cost = {"distance":None,"capacity":None}
            cost["distance"] = float(hs.haversine(location,(float(element["CapitalLatitude"]),float(element["CapitalLongitude"]))))
            cost["capacity"] = float(info_lp_cable["capacityTBPS"])
        
            mp.put(analyzer["edges"],edge_identifier,cost)

            gr.addEdge(graph, tuple_place_cablename, (city,0), cost)
    else:
        None

    sinMar(analyzer,country,city)
   
def sinMar(analyzer,country,city):
    info = mp.get(analyzer["countries"], country)["value"]
    location = (float(info["CapitalLatitude"]),float(info["CapitalLongitude"]))
    lista3 = mp.keySet(analyzer["vertices"])

    lista_final = lt.newList(datastructure="ARRAY_LIST")
    i=1
    while i<=lt.size(lista3):
        country=lt.getElement(lista3, i)
        lista2 = mp.get(analyzer["vertices"],country)["value"]
        ii = 1
        while ii<=lt.size(lista2):
    
            lp_name = lt.getElement(lista2, ii)["LP_cable"]
            lp = lt.getElement(lista2, ii)["info"]
            location_lp = mp.get(analyzer["location_dado_id"], lp_name[0])["value"]
            capacity = float(lp["capacityTBPS"])
            distance = hs.haversine(location_lp, location)
            lt.addLast(lista_final, (lp_name,distance,capacity))
            ii += 1
        i+=1
        
    lista_sorteada = mrge.sort(lista_final,cmpSinMar)
    tupla = lt.getElement(lista_sorteada, 1)
    cost = {"distance":tupla[1],"capacity":float(tupla[2])}
    gr.addEdge(analyzer["connections"], tupla[0], (city,0), cost)

def edges_same_country(analyzer):
    lista = mp.keySet(analyzer["vertices"])
    i=1
    while i<=lt.size(lista):
        country=lt.getElement(lista, i)
        lista2 = mp.get(analyzer["vertices"],country)["value"]
        ii = 1
        while ii<=lt.size(lista2):
            lp1 = lt.getElement(lista2, ii)
            lp1_name = lp1["LP_cable"]
            e = lt.size(lista2)-ii
            while e<=lt.size(lista2):
                lp2 = lt.getElement(lista2, e)
                lp2_name = lp2["LP_cable"]
                cost = {"distance":None,"capacity":None}
                cost["distance"] = float(0.1)
                cost["capacity"] = min(float(lp1["info"]["capacityTBPS"]),float(lp2["info"]["capacityTBPS"]))
                mp.put(analyzer["edges"],(lp1_name,lp2_name),cost)
                gr.addEdge(analyzer["connections"], lp1_name, lp2_name, cost)
                e +=1    
            ii+=1
        i += 1





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
    return(float(tupla1[1])>=float(tupla2[1]))


def r1(analyzer):
    newmap=mp.newMap()
    x=scc.KosarajuSCC(analyzer['connections'])
    mapa=x['idscc']
    keys=mp.keySet(mapa)
    i=1
    while i<=lt.size(keys): 
        key=lt.getElement(keys,i)
        if key!=None:
            value=mp.get(mapa,key)['value']
            par=mp.get(newmap,key[0])
            if par!=None:
                mmap=me.getValue(par)
                mp.put(mmap,value,None)
            else:
                mmap=mp.newMap()
                mp.put(mmap,value,None)
                mp.put(newmap,key[0],mmap)
            i+=1
    return newmap

def req1(analyzer,num1,num2):
    mapa=r1(analyzer)
    val1=mp.get(mapa,num1)['value']
    val2=mp.get(mapa,num2)['value']
    nums=mp.keySet(val1)
    i=1
    final=False
    centinela=True
    while i<=lt.size(nums) and centinela:
        num=lt.getElement(nums,i)
        if mp.contains(val2,num):
            centinela==False
            final=True
        i+=1
    return final
