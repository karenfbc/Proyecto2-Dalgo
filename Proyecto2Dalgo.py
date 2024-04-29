import sys
from collections import deque

def compuesto_(fundamentales, fund_organizados):
    dicc_comprobacion = {}
    for numero, etiqueta in fund_organizados:
        if numero in dicc_comprobacion:
            if dicc_comprobacion[numero] != etiqueta:
                return "NO SE PUEDE"
        else:
            dicc_comprobacion[numero] = etiqueta
    rta=iniciar_grafo(fundamentales)
    return rta

def enlace_toll(fundamentales):
    pass

def add_arco(fundamentales, start, end, grado):
    if start in fundamentales:
        fundamentales[start].append(end)
    else:
        fundamentales[start] = [end]
    if end not in fundamentales:
        fundamentales[end] = []
    if end in grado:
        grado[end] += 1
    else:
        grado[end] = 1
    if start not in grado:
        grado[start] = 0

def iniciar_grafo(fundamentales):
    graph = {}
    grado = {}
    nodos = set()

    for start, end in fundamentales:
        add_arco(graph, start, end, grado)
        nodos.update([start, end])

    return graph, grado, nodos


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
        for l in range(n):
            n1, n2 = map(int, sys.stdin.readline().strip().split())
            fundamentales.append((n1, n2))
        reorganizados = reorganizar_fund(fundamentales)
        rta = compuesto_(fundamentales,reorganizados)
        print(fundamentales)
        print(reorganizados)
        print(rta)
