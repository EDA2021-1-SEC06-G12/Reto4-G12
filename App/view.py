"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config
import model
import controller
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import cycles as ccs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1 - Cargar información en el catálogo")
    print('2 - Hallar cantidad de clústeres dentro de la red de cables submarinos y averiguar si dos landing points al mismo clúster.')


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        analyzer = controller.init()
        tupla = controller.cargar(analyzer)
        print("Número de landing points cargados: ", str(tupla[0]))
        print("El total de conexiones entre landing points: ", str(tupla[1]))
        print("Total de paises: ", str(tupla[2]))
        print
        

    elif int(inputs[0]) == 2:
        lp1=input('Ingrese el primer landing point de interés: ')
        lp2=input('Ingrese el segundo landing point de interés: ')
        x=controller.req1(analyzer,lp1.lower(),lp2.lower())
        if x!=None:
            print('\nHay un total de '+str(x[1])+' clusters en la red.\n')
            if x[0]==True:
                print(lp1.capitalize()+' y '+lp2.capitalize()+' están en el mismo cluster.\n')
            else:
                print(lp1.capitalize()+' y '+lp2.capitalize()+' no están en el mismo cluster.\n')
        else:
            print('\nNo hay información para los landing points ingresados.\n')
        input('Ingrese enter para continuar.')
        
    elif int(inputs[0]) == 4:
        pais1=input('Ingrese el primer país de interés: ')
        pais2=input('Ingrese el segundo país de interés: ')
        controller.req2(analyzer,pais1.lower(),pais2.lower())

    else:
        sys.exit(0)
sys.exit(0)
