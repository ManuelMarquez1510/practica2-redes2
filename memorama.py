# importamos librerias que utilizaremos

import sys
import time
import os
import random

# control despliegue
bDespliegue = False

# Orden del tablero
ordenTablero = 4

# Tablero
tablero = []

# Cartas
cartas = ["Arbol", "Bombo", "Caldo", "Dados", "Elote", "Fiona", "Grito", "Higos", "Impar", "Julia", "Karma",
          "Lapiz", "Manta", "Nariz", "Oreja", "Perro", "Queso", "Ratas", "Salir", "Talco", "Union", "Viejo", "Wendy",
          "Xolos", "Yarda", "Zorro"]
# Variable que indica jugador 1 activo
jugador1Activo = True

# contador de pares
scoreJugador1 = 0
scoreJugador2 = 0


# funcion para crear el tablero
def tableroCrear():
    # cliclo para generar tablero vacio
    for lineas in range(ordenTablero):

        # inicializa la linea
        linea = []

        # ciclo para las columnas
        for columnas in range(ordenTablero):
            linea.append("------")

        # agrega la linea al tablero
        tablero.append(linea)


# funcion para desplegar tablero
def tableroDesplegar(enJuego):
    # ciclo por linea
    for linea in tablero:

        # ciclo por columnas
        for palabra in linea:
            if palabra == "*J1*" or palabra == "*J2*":
                print(palabra, end="  ")
            else:
                if enJuego:
                    print("------", end="  ")
                else:
                    print(palabra, end="  ")

        # cambio de linea
        print()

    # deja una linea
    print()


# funcion para iniciar el tablero  con los numero
def tableroIniciar():
    # variable para saber si se ha llenado el tablero
    global carta
    paresColocados = 0

    # control de la carta
    bCarta2 = False

    # ciclo mientras noo este completado el tablero
    while (paresColocados < (ordenTablero * ordenTablero) / 2):

        # Ciclo para colocar la carta
        while (True):

            # Genera un numero aleatorio para la linea
            linea = random.randrange(ordenTablero)

            # Genera un numero aleatorio para la columna
            columna = random.randrange(ordenTablero)

            # si es la carta1
            if (not bCarta2):
                # obtiene la carta
                carta = random.choice(cartas)

            # verifica que no este desponible
            if (tablero[linea][columna] == '------'):

                # coloca la carta
                tablero[linea][columna] = carta

                # verifica si es la carta2
                if (bCarta2):
                    # incrementa el contador de casillasLlenadas
                    paresColocados = paresColocados + 1

                    # elimina la carta del mazo
                    if (bDespliegue):
                        print("Se elimina la carta:", carta)

                    # remueve la carta
                    cartas.remove(carta)

                    if (bDespliegue):
                        print(cartas)
                        input()

                # cambia el estado de la carta
                bCarta2 = not bCarta2

                # sale del ciclo
                break
            else:
                if (bDespliegue):
                    print("Fila:", linea, "Columna:", columna)
                    print("Pares colocados:", paresColocados)
                    tableroDesplegar(False)
                    input("choque...\n")

def activa(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col):
    activa = False

    if(J1carta1ren == J1carta2ren and J1carta1col == J1carta2col):
            activa=True
    else:
        activa=False
    return activa

# Funcion que verifica si es par

def esParJ1(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col):
    # variable para resultado
    bEsPar = False

    # compara
    if (tablero[J1carta1ren][J1carta1col] == tablero[J1carta2ren][J1carta2col]):
        # Desplega mensaje
        #print("hiciste un par")

        # coloca a que jugador pertenece el par realizado
        # coloca jugador1
        tablero[J1carta1ren][J1carta1col] = "*J1*"
        tablero[J1carta2ren][J1carta2col] = "*J1*"

        # Variable de resultado
        bEsPar = True
    #else:
        # Despliega mensaje de error
        #print("Fallaste")

    # Pausa para continuar
    #input("Presione ester para continuar...\n")
    return bEsPar

def esParJ2(J2carta1ren, J2carta1col, J2carta2ren, J2carta2col, ):
    # variable para resultado
    bEsPar = False

    # compara
    if (tablero[J2carta1ren][J2carta1col] == tablero[J2carta2ren][J2carta2col]):
        # Desplega mensaje
        #print("hiciste un par")

        # coloca a que jugador pertenece el par realizado
        tablero[J2carta1ren][J2carta1col] = "*J2*"
        tablero[J2carta2ren][J2carta2col] = "*J2*"

        # Variable de resultado
        bEsPar = True
    #else:
        # Despliega mensaje de error
        #print("Fallaste")
    # Pausa para continuar
    #print("\n")
    #input("Presione ester para continuar...\n")

    # retorna
    return bEsPar


# funcion para obtener  una carta seleccionada
def cartaSeleccionadaValida(ren, col):
    valida = True
    if (tablero[ren][col] == "*J1*" or tablero[ren][col] == "*J2*"):
        valida = False

    else:
        valida = True
    # retorna la carta seleccionada
    return valida

def cartaSeleccionada(ren,col):
    return (tablero[ren][col])

# Funcion que despliega el marcador
def marcadorDesplegar():
    print("El marcador es:")
    print("El jugador 1:", scoreJugador1)
    print("El jugador 2:", scoreJugador2)
    print()


# inicia el juego
tableroCrear()

print("Tablero a jugar")
print()
tableroDesplegar(False)

# iniciar el tablero
tableroIniciar()

print("Cartas a jugar")
print()

tableroDesplegar(False)



# ciclo de juego


while (scoreJugador1 + scoreJugador2 < ordenTablero * ordenTablero / 2):

    if(jugador1Activo==True):
        while True:
            print("Jugador 1 activo")
            # solicita la jugada
            print("\ncapture la posicion de la primera carta: renglon, columna")
            jugada = input()

            # convirtiendo a listas
            listaJugadas = jugada.split(",")

            # obtiendo las coordenadas de la carta1
            J1carta1ren = int(listaJugadas[0])
            J1carta1col = int(listaJugadas[1])

            if (cartaSeleccionadaValida(J1carta1ren, J1carta1col) == True):
                # despliega lo que hay en esa posicion
                print("La carta 1 seleccionada es:", cartaSeleccionada(J1carta1ren, J1carta1col))
                valida = True
            else:
                print("la carta esta en juego, vuelva a intentarlo...\n")
                tableroDesplegar(True)
                valida = False
                if valida == False:
                    continue
            while True:
                print("\nCapture la posicion de la segunda carta: renglon, columna")
                jugada = input()
                # convirtiendo a listas
                listaJugadas = jugada.split(",")

                # obtiendo las coordenadas de la carta2
                J1carta2ren = int(listaJugadas[0])
                J1carta2col = int(listaJugadas[1])
                if(activa(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col)):
                    print("la carta esta en juego, vuelva a intentarlo...\n")
                    tableroDesplegar(True)
                    continue
                else:
                    if (cartaSeleccionadaValida(J1carta2ren, J1carta2col) == True):
                        # despliega lo que hay en esa posicion
                        print("La carta 2 seleccionada es:", cartaSeleccionada(J1carta2ren, J1carta2col))
                        valida = True
                    else:
                        print("la carta esta en juego, vuelva a intentarlo...\n")
                        tableroDesplegar(True)
                        valida = False
                        if valida == False:
                            continue
                    if valida:
                        break

            if (esParJ1(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col)):
                print("\n¡Hiciste par!\n")
                # incrementa el contador del jugador 1
                scoreJugador1 = scoreJugador1 + 1
                tableroDesplegar(True)
                marcadorDesplegar()
                jugador1Activo = True
                if (scoreJugador1 + scoreJugador2 >= ordenTablero * ordenTablero / 2):
                    break
            else:
                print("\n¡Fallaste!\n")
                jugador1Activo = False

            if jugador1Activo == False:
                break
            # despliega el tablero y el marcador
        tableroDesplegar(True)
        marcadorDesplegar()

    elif (jugador1Activo == False):
        while True:
            print("Jugador 2 activo")
            if (ordenTablero == 4):
                # obtiendo las coordenadas de la
                J2carta1ren = random.randrange(4)
                J2carta1col = random.randrange(4)
            else:
                J2carta1ren = random.randrange(0, 6)
                J2carta1col = random.randrange(0, 6)
            if(cartaSeleccionadaValida(J2carta1ren,J2carta1col)==True):
                # despliega lo que hay en esa posicion
                print("La carta 1 seleccionada es:", cartaSeleccionada(J2carta1ren, J2carta1col))
                valida =True
            else:
                #print("la carta esta en juego, vuelva a intentarlo...")
                valida = False
                if valida == False:
                    continue
            while True:
                if(ordenTablero==4):

                    J2carta2ren = random.randrange(4)
                    J2carta2col = random.randrange(4)
                else:
                    J2carta2ren = random.randrange(6)
                    J2carta2col = random.randrange(6)

                if (activa(J2carta1ren, J2carta1col, J2carta2ren, J2carta2col)):
                    #print("la carta esta en juego, vuelva a intentarlo...colaa")
                    continue
                else:
                    if (cartaSeleccionadaValida(J2carta2ren, J2carta2col) == True):
                        # despliega lo que hay en esa posicion
                        print("La carta 2 seleccionada es:", cartaSeleccionada(J2carta2ren, J2carta2col))
                        valida = True
                    else:
                        #print("la carta esta en juego, vuelva a intentarlo...")
                        valida =False
                        if valida == False:
                            continue
                    if valida:
                        break

            # llama a funcion que verifica si coinciden
            if (esParJ2(J2carta1ren, J2carta1col, J2carta2ren, J2carta2col)):
                # incrementa el contador del jugador 2
                print("\n¡Hiciste par!\n")
                scoreJugador2 = scoreJugador2 + 1
                tableroDesplegar(True)
                marcadorDesplegar()
                jugador1Activo = False
                if (scoreJugador1 + scoreJugador2 >= ordenTablero * ordenTablero / 2):
                    break
            else:
                print("\n!Fallaste!\n")
                jugador1Activo = True

            if jugador1Activo == True:
                break
        # despliega el tablero y el marcador
        tableroDesplegar(True)
        marcadorDesplegar()

# validacion final
if (scoreJugador1 > scoreJugador2):
    print("El jugador 1 ha ganado")

else:
    if (scoreJugador2 > scoreJugador1):
        print("El jugador 2 ha ganado")
    else:
        print("Ha sido un empate")
