
import socket
import time
import pickle
import random
import sys


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
            if palabra == "**JJ**" or palabra == "**J2**":
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

# Funcion que despliega el marcador
def marcadorDesplegar():
    print("Marcador:")
    print("Jugador :", scoreJugador1)
    print()


scoreJugador1=0

tablero = []
jugadorActivo = True
HOST = "localhost"  # The server's hostname or IP address
PORT = 8011  # The port used by the server
buffer_size = 1024
puntaje = 0
ordenTablero = 2
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Esperando que se conecten los demas jugadores...\n")


    while True:
        try:
            print("recibiendo tablero...")
            # Recibe el tablero del servidor
            tablero = pickle.loads(TCPClientSocket.recv(buffer_size))
            print("tablero recibido correctamente")
            tFinal = TCPClientSocket.recv(buffer_size)
            tFinalDecode = tFinal.decode("utf-8")
            #print(f"TFINAL={tFinalDecode}")
            if(tFinalDecode=="si"):
                print()
                break
        except Exception as e:
            break

        print("Tablero a jugar")
        print()
        tableroDesplegar(True)
        sys.stdout.flush()
        jugada = input("Ingrese la primera carta: renglon, columna: \n")
        # convirtiendo a listas
        listaJugadas = jugada.split(",")
        # obtiendo las coordenadas de la carta1
        J1carta1ren = int(listaJugadas[0])
        J1carta1col = int(listaJugadas[1])
        # enviando datos  1
        TCPClientSocket.send(jugada.encode('utf-8'))
        # recibiendo datos 1
        cartasRecibir = TCPClientSocket.recv(buffer_size)
        cartasRecibirDecode = cartasRecibir.decode('utf-8')
        listaCartas = cartasRecibirDecode.split("*")
        cartaValida = listaCartas[0]
        # print(cartaValida)
        cartaSeleccionada = listaCartas[1]
        # print(cartaSeleccionada)
        if cartaValida == "cartaValida1On":
            print("La carta 1 seleccionada es:", cartaSeleccionada, "\n")
            valida = True
        else:
            print("la carta seleccionada esta en juego, vuelva a intentarlo...")
            tableroDesplegar(True)
            valida = False
            continue
        while True:
            sys.stdout.flush()
            jugada = input("Ingrese la segunda carta: renglon, columna: \n")
            # convirtiendo a listas
            listaJugadas = jugada.split(",")
            # obtiendo las coordenadas de la carta1
            J1carta2ren = int(listaJugadas[0])
            J1carta2col = int(listaJugadas[1])
            TCPClientSocket.send(jugada.encode('utf-8'))
            sys.stdout.flush()
            cartasRecibir = TCPClientSocket.recv(buffer_size)
            cartasRecibirDecode = cartasRecibir.decode('utf-8')
            listaCartas = cartasRecibirDecode.split("*")
            cartaValida = listaCartas[1]
            # print(cartaValida)
            cartaSeleccionada = listaCartas[2]
            # print(cartaSeleccionada)
            cartaActiva = listaCartas[0]
            print("carta activa: ",cartaActiva)
            if cartaActiva == "cartaActiva1On":
                print("la carta seleccionada esta en juego, vuelva a intentarlo...")
                tableroDesplegar(True)
                continue
            else:
                # print("carta valida 2: ", cartaValida)
                if cartaValida == "cartaValida2On":
                    print("La carta 2 seleccionada del jugador es: ", cartaSeleccionada, "\n")
                    valida = True
                else:
                    print("la carta seleccionada esta en juego, vuelva a intentarlo...")
                    tableroDesplegar(True)
                    valida = False
                    continue
                if valida:
                    break
        par = TCPClientSocket.recv(buffer_size)
        parDecode = par.decode('utf-8')
        if (parDecode == "esPar1"):
            # incrementa el contador del jugador 1
            print("\n¡El jugador  hizo par!\n")
            scoreJugador1 = scoreJugador1 + 1
            jugadorActivo = True
            marcadorDesplegar()
        else:
            print("\n¡El jugador Fallo!\n")
            jugadorActivo = False

    # despliega el tablero y el marcador
    tableroDesplegar(True)
    marcadorDesplegar()
    jugador = TCPClientSocket.recv(buffer_size)
    if jugador.decode('utf-8') == "jugador1":
        print("El jugador 1 ha ganado")
    else:
        if jugador.decode('utf-8') == "jugador2":
            print("El jugador 2 ha ganado")
        else:
            print("El jugador 3 ha ganado")

print("Termino la partida")