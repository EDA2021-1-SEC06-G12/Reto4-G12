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
import sys
assert config


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("1 — Cargar información en el catálogo")
    print('2 — Hallar cantidad de clústeres dentro de la red de cables submarinos y averiguar si dos landing points pertenecen al mismo clúster.')
    print('3 — Hallar los landing points que sirven como punto de interconexión a más cables en la red.')
    print('4 — Hallar ruta mínima en distancia para enviar información entre dos países.')
    print('5 — Identificar la infraestructura crítica para poder garantizar su mantenimiento preventivo.')
    print('6 — Conocer impacto que tendría el fallo de un determinado landing point que afecta a todos sus cables conectados.')
    print('7 — Conocer el ancho de banda máximo que se puede garantizar para la transmisión de un servidor ubicado en un país desde todos los países conectados a un cable.')
    print('0 — Salir')



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('\nSeleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("")
        print("Cargando información de los archivos ....")
        analyzer = controller.init()
        tupla = controller.cargar(analyzer)
        print("\nNúmero de landing points cargados: ", str(tupla[0]))
        print("El total de conexiones entre landing points: ", str(tupla[1]))
        print("Total de paises: ", str(tupla[2]))
        input('\nPresione enter para continuar.\n')
        
        
    elif int(inputs[0]) == 2:
        print("")
        lp1=input('Ingrese el primer landing point de interés (ciudad, pais): ')
        lp2=input('Ingrese el segundo landing point de interés (ciudad, pais): ')
        x=controller.req1(analyzer,lp1.lower(),lp2.lower())
        if x!=None:
            print('\nHay un total de '+str(x[0][0])+' clusters en la red.\n')
            if x[0][1]==True:
                print(lp1.capitalize()+' y '+lp2.capitalize()+' están en el mismo cluster.\n')
            else:
                print(lp1.capitalize()+' y '+lp2.capitalize()+' no están en el mismo cluster.\n')
        else:
            print('\nNo hay información para los landing points ingresados.\n')
        
        print("Tiempo [ms]: "+f"{x[1]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[2]:.3f}"+'\n')
        input('\nPresione enter para continuar.\n')
    

    elif int(inputs[0]) == 3:
        print('')
        x = controller.req2(analyzer)
        print('')
        print("Tiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')
        print('')
        input('\nPresione enter para continuar.\n')


    elif int(inputs[0]) == 4:
        print("")
        pais1=input('Ingrese el primer país de interés: ')
        pais2=input('Ingrese el segundo país de interés: ')
        x = controller.req3(analyzer,pais1,pais2)
        print('')
        print("Tiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')
        print('')
        input('\nPresione enter para continuar.')


    elif int(inputs[0]) == 5: 
        print("")
        x = controller.req4(analyzer)
        print('')
        print("Tiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')
        print('')
        input('\nPresione enter para continuar.\n')


    elif int(inputs[0]) == 6: 
        print("")
        lp_name = str(input("Ingrese el landing point donde ocurriria el fallo: ")).lower()
        x = controller.req5(analyzer,lp_name)
        print('')
        print("Tiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')
        print('')
        input('\nPresione enter para continuar.\n')


    elif int(inputs[0]) == 7: 
        print("")
        pais = str(input("Ingrese el nombre del país (pais): ")).lower()
        cable = str(input("Ingrese el nombre del cable (el nombre debe ser exactamente el mismo): "))
        x = controller.req6(analyzer,pais,cable)
        print('')
        print("Tiempo [ms]: "+f"{x[0]:.3f}"+" ||  "+"Memoria [kB]: "+f"{x[1]:.3f}"+'\n')
        print('')
        input('\nPresione enter para continuar.\n')

    else:
        sys.exit(0)
sys.exit(0)
