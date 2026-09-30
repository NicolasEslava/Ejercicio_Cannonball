import math


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Destino:
    def __init__(self, x, y, cañon):
        self.x = x
        self.y = y
        self.cañon = cañon


class ListaCircular:
    def __init__(self):
        self.ultimo = None

    def vacia(self):
        return self.ultimo is None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self.vacia():
            self.ultimo = nuevo
            nuevo.siguiente = nuevo
        else:
            nuevo.siguiente = self.ultimo.siguiente
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo

    def convertir_lista(self):
        puntos = []
        if self.vacia():
            return puntos

        primero = self.ultimo.siguiente
        actual = primero

        while True:
            puntos.append(actual.dato)
            actual = actual.siguiente
            if actual == primero:
                break
        return puntos

    def mostrar(self):

        if self.vacia():
            print("Lista vacia")
            return

        primero = self.ultimo.siguiente
        actual = primero

        while True:
            print(actual.dato)
            actual = actual.siguiente
            if actual == primero:
                break


def distancia(punto1, punto2):
    return math.sqrt((punto2.x - punto1.x)**2 + (punto2.y - punto1.y)**2)


def tiempo_corriendo(punto1, punto2):
    d = distancia(punto1, punto2)/5
    return d


def tiempo_cañon(punto1, punto2):
    d = distancia(punto1, punto2)
    return 2 + abs(d - 50)/5  # valor absoluto


def mejor_tiempo(punto1, punto2):
    correr = tiempo_corriendo(punto1, punto2)

    if punto1.cañon:
        cañon = tiempo_cañon(punto1, punto2)
        return min(correr, cañon)  # devuelve el valor minimo

    return correr


def buscar_menor(tiempos, visitados):
    posicion = -1

    for i in range(len(tiempos)):
        if not visitados[i]:
            if posicion == -1 or tiempos[i] < tiempos[posicion]:
                posicion = i

    return posicion


def calcular_tiempo(lista):
    puntos = lista.convertir_lista()
    cantidad = len(puntos)

    tiempos = [float("inf")] * cantidad
    visitados = [False] * cantidad

    tiempos[0] = 0

    for _ in range(cantidad):

        actual = buscar_menor(tiempos, visitados)
        print("Visitando:", actual, "Tiempo:", tiempos[actual])

        if actual == -1:
            break

        visitados[actual] = True

        for i in range(cantidad):
            if not visitados[i]:

                tiempo = mejor_tiempo(puntos[actual], puntos[i])
                nuevo_tiempo = tiempos[actual] + tiempo

                if nuevo_tiempo < tiempos[i]:
                    tiempos[i] = nuevo_tiempo

    return tiempos[cantidad - 1]


x_inicio, y_inicio = map(float, input().split())
x_final, y_final = map(float, input().split())

lista = ListaCircular()

lista.agregar(Destino(x_inicio, y_inicio, False))

cantidad_cañones = int(input())

for _ in range(cantidad_cañones):
    x, y = map(float, input().split())
    lista.agregar(Destino(x, y, True))

lista.agregar(Destino(x_final, y_final, False))

resultado = calcular_tiempo(lista)

print(f"{resultado:.6f}")
