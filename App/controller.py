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
    
    
    countriesfile = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(countriesfile, encoding="utf-8"),
                                delimiter=",")
    for country in input_file:
        mp.put(analyzer["countries"],country["CountryName"],country)
        model.addCapital_V_E(analyzer,country)
    
    model.edges_same_country(analyzer)

    
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
    
