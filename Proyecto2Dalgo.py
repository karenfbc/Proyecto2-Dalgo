import sys
from collections import defaultdict, deque

def compuesto_(fundamentales, fund_organizados, libres, w1, w2):
    dicc_comprobacion = {}

    for numero, etiqueta in fund_organizados:
        if numero in dicc_comprobacion:
            if dicc_comprobacion[numero] != etiqueta:
                return "NO SE PUEDE"
        else:
            dicc_comprobacion[numero] = etiqueta

    fundamentales_ordenados = camino_euler(fundamentales)
    print(fundamentales_ordenados)
    fund_toll= enlace_toll(fundamentales_ordenados)
    consulta_camino = energia_necesaria(libres, w1, w2, fundamentales)
    costoT=0
    camino = []
    for i in range(0,len(fund_toll)-1,2):
        nod1=fund_toll[i][1]
        nod2=fund_toll[i+1]
        pos1= libres.index(nod1)
        pos2= libres.index(nod2)
        costo_camino, caminos = consulta_camino(pos1, pos2)  # Consultar el camino de 2 a 5, por ejemplo
        camino.append(fund_toll[i])
        costoT+=costo_camino
        for j in caminos[1:]:
            camino.append(libres[j])
    camino.append(fund_toll[-1])
    print(costoT)
    print("Camino:", camino)
    #caminoMinimo=floyd_warshall(energia)
    #print(caminoMinimo)

    return fund_toll

def camino_euler(fundamentales):
    grafo = defaultdict(list)
    aristas = defaultdict(int)
    for u, v in fundamentales:
        grafo[u].append(v)
        grafo[v].append(u)
        aristas[u] += 1
        aristas[v] += 1

    inicio = fundamentales[0][0]
    for nodo in aristas:
        if aristas[nodo] % 2 != 0:
            inicio = nodo
            break

    def dfs(v):
        stack = [v]
        camino = []
        while stack:
            nodo = stack[-1]
            if grafo[nodo]:
                nodo_sig = grafo[nodo].pop()
                grafo[nodo_sig].remove(nodo)
                stack.append(nodo_sig)
            else:
                camino.append(stack.pop())
        return camino[::-1]

    camino = dfs(inicio)

    parejas_camino = []
    for i in range(len(camino) - 1):
        parejas_camino.append((camino[i], camino[i + 1]))

    return parejas_camino

def enlace_toll(fundamentales):
    resultado = []
    resultado.append(fundamentales[0])

    for i in range(1, len(fundamentales)):
        nodo_intermedio = -fundamentales[i-1][1]
        resultado.append(nodo_intermedio)
        resultado.append(fundamentales[i])
    return resultado

"""def floyd_warshall(grafo):
    graph_size = len(grafo)
    for initial in range(0,graph_size) :
        for middle in range(0,graph_size) :
            for end in range(0,graph_size) :
                grafo[initial][end] = min(grafo[initial][end],
                                          grafo[initial][middle] + grafo[middle][end])
    return grafo"""

def calcular_ltp(m1, c1, m2, c2, w1, w2):
    if c1 == c2:
        return 1 + abs(m1 - m2) % w1
    else:
        return w2 - abs(m1 - m2) % w2
    
def energia_necesaria(libres, w1, w2, fundamentales):
    n = len(libres)
    dp = [[float('inf')] * n for _ in range(n)]
    next = [[-1] * n for _ in range(n)]
    
    # Inicializar la matriz de costos y la matriz de rutas
    for i in range(n):
        for j in range(n):
            if (libres[i], libres[j]) in fundamentales or abs(libres[i]) == abs(libres[j]):
                dp[i][j] = 10000
            elif (libres[i] < 0 and libres[j] < 0) or (libres[i] >= 0 and libres[j] >= 0):
                m1 = abs(libres[i])
                m2 = abs(libres[j])
                dp[i][j] = calcular_ltp(m1, "igual", m2, "igual", w1, w2)
            elif (libres[i] < 0 and libres[j] >= 0) or (libres[i] >= 0 and libres[j] < 0):
                m1 = abs(libres[i])
                m2 = abs(libres[j])
                dp[i][j] = calcular_ltp(m1, "positivo", m2, "negativo", w1, w2)
            if dp[i][j] != float('inf'):
                next[i][j] = j

    # Algoritmo de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dp[i][j] > dp[i][k] + dp[k][j]:
                    dp[i][j] = dp[i][k] + dp[k][j]
                    next[i][j] = next[i][k]

    # Función para obtener el camino
    def get_path(i, j):
        if next[i][j] == -1:
            return []
        path = [i]
        while i != j:
            i = next[i][j]
            path.append(i)
        return path

    # Función para consultar el camino y el costo entre dos vértices específicos
    def consulta_camino(origen, destino):
        if origen < 0 or destino < 0 or origen >= n or destino >= n:
            return "Índices fuera de rango", []
        if dp[origen][destino] == float('inf'):
            return "No hay camino disponible", []
        camino = get_path(origen, destino)
        costo = dp[origen][destino]
        return costo, camino
    
    return consulta_camino


def reorganizar_fund(fundamentales):
    fund_reorganizado = []
    for inicio, final in fundamentales:
        fund_reorganizado.append((abs(inicio), "positivo" if inicio >= 0 else "negativo"))
        fund_reorganizado.append((abs(final), "positivo" if final >= 0 else "negativo"))
    return fund_reorganizado

if __name__ == "__main__":
    number_of_cases = int(sys.stdin.readline().strip())
    for _ in range(number_of_cases):
        n, w1, w2 = map(int, sys.stdin.readline().split())
        fundamentales = []
        libres=[]
        for l in range(n):
            n1, n2 = map(int, sys.stdin.readline().strip().split())
            fundamentales.append((n1, n2))
            if n1 not in libres:
                libres.append(n1)
                libres.append(-n1)
            if n2 not in libres:
                libres.append(n2)
                libres.append(-n2)
        reorganizados = reorganizar_fund(fundamentales)
        rta = compuesto_(fundamentales,reorganizados,libres,w1,w2)
        print(fundamentales)
        print(reorganizados)
        print(libres)
        print(rta)

