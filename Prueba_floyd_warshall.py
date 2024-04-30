def floyd_warshall(weights):
    n = len(weights)
    dist = [row[:] for row in weights]  # Copia la matriz original

    # Actualizar distancias usando el algoritmo de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

# Matriz de adyacencia del grafo
weights = [
    [10000, 10000, 3, 3, 5, 3, 0, 4],
    [10000, 10000, 3, 3, 3, 5, 4, 1],
    [0, 3, 10000, 10000, 2, 1, 2, 1],
    [3, 3, 10000, 10000, 1, 2, 1, 2],
    [5, 3, 0, 1, 10000, 10000, 4, 2],
    [3, 5, 1, 2, 10000, 10000, 2, 4],
    [1, 4, 2, 1, 4, 2, 10000, 10000],
    [4, 1, 1, 2, 2, 4, 10000, 10000]
]

# Aplicar el algoritmo de Floyd-Warshall
result = floyd_warshall(weights)

# Imprimir la matriz de distancias resultante
for row in result:
    print(row)
