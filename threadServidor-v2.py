# !/usr/bin/env python3

import socket
import sys
import threading
import pickle
import random
import logging
from collections import deque

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
#funciones del juego


# Variable que indica jugador 1 activo
jugador1Activo = True

# contador de pares
scoreJugador1 = 0
# control despliegue
bDespliegue = False
def tableroCrear():
    # cliclo para generar tablero vacio
    for lineas in range(ordenTablero):

        # inicializa la linea
        linea = []

        # ciclo para las columnas
        for columnas in range(ordenTablero):
            linea.append("------")

        # agrega la linea al tablero
        t.tablero.append(linea)


# funcion para desplegar tablero
def tableroDesplegar(enJuego):
    # ciclo por linea
    for linea in t.tablero:

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


# funcion para iniciar el tablero  con los numero
def tableroIniciar():
    # variable para saber si se ha llenado el tablero
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
                t.carta = random.choice(t.cartas)

            # verifica que no este desponible
            if (t.tablero[linea][columna] == '------'):

                # coloca la carta
                t.tablero[linea][columna] = t.carta

                # verifica si es la carta2
                if (bCarta2):
                    # incrementa el contador de casillasLlenadas
                    paresColocados = paresColocados + 1

                    # elimina la carta del mazo
                    if (bDespliegue):
                        print("Se elimina la carta:", t.carta)

                    # remueve la carta
                    t.cartas.remove(t.carta)

                    if (bDespliegue):
                        print(t.cartas)
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

    if (J1carta1ren == J1carta2ren and J1carta1col == J1carta2col):
        activa = True
    else:
        activa = False
    return activa


# Funcion que despliega el marcador
def marcadorDesplegar():
    print("Marcador:")
    print("Jugador 1:", t.j1)
    print("Jugador 2:", t.j2)
    print("Jugador 3:", t.j3)
    print()

class Tablero(object):
    def __init__(self):
        self.j1=0
        self.j2 = 0
        self.j3 = 0
        self.puntajeTotal = 0
        self.mutex = threading.Lock()
        self.carta = None
        self.tablero = []
        self.cartas = ["Arbol", "Bombo", "Caldo", "Dados", "Elote", "Fiona", "Grito", "Higos", "Impar", "Julia", "Karma",
          "Lapiz", "Manta", "Nariz", "Oreja", "Perro", "Queso", "Ratas", "Salir", "Talco", "Union", "Viejo", "Wendy",
          "Xolos", "Yarda", "Zorro"]

    def esParJ1(self, J1carta1ren, J1carta1col, J1carta2ren, J1carta2col):
        # variable para resultado
        bEsPar = False
        #compara
        if (self.tablero[J1carta1ren][J1carta1col] == self.tablero[J1carta2ren][J1carta2col]):
            logging.debug("Esperando a adquirir el candado de la seccion critica")
            self.mutex.acquire()
            try:
                logging.debug("Candado adquirido de la region critica")
                self.tablero[J1carta1ren][J1carta1col] = "**JJ**"
                self.tablero[J1carta2ren][J1carta2col] = "**JJ**"
                self.puntajeTotal = self.puntajeTotal + 1
                logging.debug(f" El {threading.current_thread().name} consiguio un punto")
                if threading.current_thread().name == "jugador 1":
                    self.j1 = self.j1+1
                elif threading.current_thread().name == "jugador 2":
                    self.j2=self.j2+1
                elif threading.current_thread().name == "jugador 3":
                    self.j3=self.j3+1

                # Variable de resultado
                bEsPar = True

            finally:
                self.mutex.release()
                logging.debug("Candado de la seccion critica liberado ")
                return bEsPar

    def esParJ2(self,J2carta1ren, J2carta1col, J2carta2ren, J2carta2col):
        # variable para resultado
        bEsPar = False

        # compara
        if (self.tablero[J2carta1ren][J2carta1col] == self.tablero[J2carta2ren][J2carta2col]):
            # coloca a que jugador pertenece el par realizado
            self.tablero[J2carta1ren][J2carta1col] = "**J2**"
            self.tablero[J2carta2ren][J2carta2col] = "**J2**"

            # Variable de resultado
            bEsPar = True

        return bEsPar

    # funcion para obtener  una carta seleccionada
    def cartaSeleccionadaValida(self,ren, col):
        valida = True
        if (self.tablero[ren][col] == "**JJ**" or self.tablero[ren][col] == "**J2**"):
            valida = False

        else:
            valida = True
        # retorna la carta seleccionada
        return valida

    def cartaSeleccionada(self, ren, col):
        return (self.tablero[ren][col])


#ordenTablero = 4

#funciones del servidor multiconexion

def servirPorSiempre(socketTcp, listaconexiones,semaforo,t):
    cola = deque()
    barrier = threading.Barrier(int(numConn))
    try:
        print("\nGenerando tablero...")
        print("creando tablero")
        tableroCrear()
        print("tablero creado exitosamente")
        print("iniciando tablero")
        tableroIniciar()
        print("tablero iniciado correctamente")
        print("\nCartas a jugar")
        tableroDesplegar(False)
        print("\n")
        print("Esperando a que se conecten los demas jugadores..\n")
        while True:
            client_conn, client_addr = socketTcp.accept()
            #print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            #print(len(listaconexiones))
            indiceJ=len(listaconexiones)
            thread_read = threading.Thread(name="jugador " + str(indiceJ),target=recibir_datos, args=[client_conn, client_addr,barrier,semaforo,t,cola])
            cola.append(thread_read.name)
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    #print("hilos activos:", threading.active_count())
    #print("enum", threading.enumerate())
    #print("conexiones: ", len(listaconexiones))
    #print(listaconexiones)

#canal de comunicacion exclusivo
def recibir_datos(Client_conn, Client_addr,barrier,semaforo,t,cola):
    global jugador1Activo
    jugador1Activo = False
    global scoreJugador1
    global valida
    global bandera
    global tFinal
    bandera = False
    cont = 1
    print(f"Esperando a que se conecten {barrier.parties-barrier.n_waiting} jugadores para iniciar la partida...")
    barrier.wait()
    try:
        print("\tPartida empezada\n\t")

        while True:

            while threading.current_thread().name not in cola[0]:
                if (t.puntajeTotal == (ordenTablero * ordenTablero) /2):
                    semaforo.release()
                    logging.debug("Candado liberado")
                    break
                else:
                    pass

            if bandera == True:
                semaforo.release()
                logging.debug("b- candado liberado")

            print()
            logging.debug("Esperando candado")
            semaforo.acquire()
            logging.debug("candado adquirido")


            if (t.puntajeTotal == (ordenTablero * ordenTablero) /2):
                semaforo.release()
                logging.debug("candado adquirido")
                break

            #print(f"puntaje total={t.puntajeTotal}")
            print("Le toca al jugador", threading.current_thread().name)
            print("enviando tablero...")
            Client_conn.send(pickle.dumps(t.tablero))
            tFinal = "no"
            Client_conn.send(tFinal.encode("utf-8"))
            print("Tablero enviado correctamente")
            sys.stdout.flush()
            print(f"\nRecibiendo el par de casillas de la primera carta del {threading.current_thread().name}...")
            # recibiendo datos 1
            jugada = Client_conn.recv(buffer_size)

            jugadaDecode = jugada.decode('utf-8')
            listaJugada = jugadaDecode.split(",")
            J1carta1ren = int(listaJugada[0])
            J1carta1col = int(listaJugada[1])
            #print(f"x = {J1carta1ren} , y = {J1carta1col} ")
            #print(f"Enviando {listaJugada} a {Client_addr}")

            if (t.cartaSeleccionadaValida(J1carta1ren, J1carta1col) == True):
                # despliega lo que hay en esa posicion
                cartaValida = "cartaValida1On"

                # enviando datos 2
                cartasEnviar = cartaValida + "*" + t.cartaSeleccionada(J1carta1ren, J1carta1col)
                Client_conn.send(cartasEnviar.encode('utf-8'))
                valida = True
            else:
                print(f"la carta seleccionada del {threading.current_thread().name} esta en juego, vuelva a intentarlo...")
                tableroDesplegar(True)
                cartaValida = "cartaValida1Off"
                cartasEnviar = cartaValida + "*" + t.cartaSeleccionada(J1carta1ren, J1carta1col)
                # enviando datos 2
                Client_conn.send(cartasEnviar.encode('utf-8'))
                bandera= True

                valida = False
                continue
            while True:
                sys.stdout.flush()
                print(f"\nRecibiendo el par de casillas de la segunda carta del {threading.current_thread().name}...")
                # recibiendo datos 2
                jugada = Client_conn.recv(buffer_size)

                jugadaDecode = jugada.decode('utf-8')
                #print("esta es la jugada decode:", jugadaDecode)
                listaJugada = jugadaDecode.split(",")
                J1carta2ren = int(listaJugada[0])
                J1carta2col = int(listaJugada[1])
                #print(f"x = {J1carta2ren} , y = {J1carta2col} ")
                #print(f"Enviando {listaJugada} a {Client_addr}")

                if (activa(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col)):
                    cartaActiva = "cartaActiva1On"
                    cartaValida = "cartaValida2Off"
                    # enviando datos 3
                    cartasEnviar = cartaActiva + "*" + cartaValida + "*" + t.cartaSeleccionada(J1carta2ren,
                                                                                               J1carta2col)
                    Client_conn.send(cartasEnviar.encode('utf-8'))
                    print(f"la carta seleccionada del {threading.current_thread().name} esta en juego, vuelva a intentarlo...")
                    tableroDesplegar(True)
                    continue
                else:
                    if (t.cartaSeleccionadaValida(J1carta2ren, J1carta2col) == True):
                        # despliega lo que hay en esa posicion
                        cartaActiva = "cartaActiva1Off"
                        cartaValida = "cartaValida2On"
                        cartasEnviar = cartaActiva + "*" + cartaValida + "*" + t.cartaSeleccionada(J1carta2ren,
                                                                                                   J1carta2col)
                        # enviando datos 4
                        Client_conn.send(cartasEnviar.encode('utf-8'))
                        valida = True
                    else:
                        print(f"la carta seleccionada del {threading.current_thread().name} esta en juego, vuelva a intentarlo...")
                        cartaActiva = "cartaActiva1Off"
                        cartaValida = "cartaValida2Off"
                        cartasEnviar = cartaActiva + "*" + cartaValida + "*" + t.cartaSeleccionada(J1carta2ren,
                                                                                                   J1carta2col)
                        Client_conn.send(cartasEnviar.encode('utf-8'))
                        tableroDesplegar(True)
                        valida = False
                        continue
                    if valida:
                        break
            if (t.esParJ1(J1carta1ren, J1carta1col, J1carta2ren, J1carta2col)):
                print(f"\n¡El {threading.current_thread().name} hizo par!\n")
                par = "esPar1"
                Client_conn.send(par.encode('utf-8'))
                #logging.debug("data enviada")
                jugador1Activo = True
                semaforo.release()
                logging.debug("Candado liberado")

            else:
                print(f"\n¡El {threading.current_thread().name} Fallo!\n")
                par = "noPar1"
                Client_conn.send(par.encode('utf-8'))
                jugador1Activo = False

            if(jugador1Activo == False):
                semaforo.release()
                logging.debug("Candado liberado")
                hilo = cola.popleft()
                cola.append(hilo)
        print("enviando tablero final...")
        Client_conn.send(pickle.dumps(t.tablero))
        tFinal = "si"
        Client_conn.send(tFinal.encode("utf-8"))
        print("Tablero final enviado correctamente")
        marcadorDesplegar()
        # validacion final
        if (t.j1 > t.j2):
            print("El jugador 1 ha ganado")
            jugador1 = "jugador1"
            Client_conn.send(jugador1.encode('utf-8'))
        else:
            if (t.j2 > t.j1):
                jugador2 = "jugador2"
                Client_conn.send(jugador2.encode('utf-8'))
                print("El jugador 2 ha ganado")
            else:
                print("El jugador 3 ha ganado")

    finally:
        Client_conn.close()




listaConexiones = []
host = "localhost"
port = 8011
buffer_size = 1024
t=Tablero()
serveraddr = (host, int(port))

print("ingrese el numero de jugadores que jugaran: ")
numConn = input()
ordenTablero = 4
valida = bool
bandera = bool
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((host, port))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")
    semaforo = threading.Semaphore(1)
    servirPorSiempre(TCPServerSocket, listaConexiones,semaforo,t)