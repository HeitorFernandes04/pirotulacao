# Rotulacao de componentes conectadas em imagem binaria
# Processamento de Imagens - UFT
# Heitor Fernandes e Mauricio Monteiro

import numpy as np


def binarizar(img, limiar=127):
    # deixa a imagem so com dois valores: 0 (fundo) e 255 (objeto)
    if img.ndim == 3:
        img = img.mean(axis=2)

    m, n = img.shape
    saida = np.zeros((m, n), dtype=np.uint8)
    for i in range(m):
        for j in range(n):
            if img[i][j] < limiar:
                saida[i][j] = 0
            else:
                saida[i][j] = 255
    return saida


def raiz(pai, r):
    # sobe ate achar o rotulo que representa o grupo
    while pai[r] != r:
        r = pai[r]
    return r


def unir(pai, a, b):
    # marca que os dois rotulos sao do mesmo objeto
    # o menor deles fica sendo o representante do grupo
    ra = raiz(pai, a)
    rb = raiz(pai, b)
    if ra < rb:
        pai[rb] = ra
    elif rb < ra:
        pai[ra] = rb


def rotular(img, cs=255, conectividade=4):
    m, n = img.shape
    rotulos = np.zeros((m, n), dtype=int)
    pai = {}          # guarda quais rotulos sao equivalentes
    proximo = 1       # proximo rotulo livre

    # primeira varredura: da esquerda para a direita, de cima para baixo
    for i in range(m):
        for j in range(n):
            if img[i][j] != cs:
                continue

            # olha so os vizinhos que a varredura ja passou
            vizinhos = []
            if j > 0 and rotulos[i][j - 1] > 0:
                vizinhos.append(int(rotulos[i][j - 1]))          # esquerda
            if i > 0 and rotulos[i - 1][j] > 0:
                vizinhos.append(int(rotulos[i - 1][j]))          # cima
            if conectividade == 8:
                if i > 0 and j > 0 and rotulos[i - 1][j - 1] > 0:
                    vizinhos.append(int(rotulos[i - 1][j - 1]))  # diagonal esq
                if i > 0 and j < n - 1 and rotulos[i - 1][j + 1] > 0:
                    vizinhos.append(int(rotulos[i - 1][j + 1]))  # diagonal dir

            if len(vizinhos) == 0:
                # nenhum vizinho rotulado, entao comeca um objeto novo
                rotulos[i][j] = proximo
                pai[proximo] = proximo
                proximo += 1
            else:
                # pega o menor rotulo dos vizinhos
                menor = min(vizinhos)
                rotulos[i][j] = menor
                # se os vizinhos tinham rotulos diferentes, e tudo o mesmo objeto
                for v in vizinhos:
                    unir(pai, menor, v)

    # segunda varredura: troca cada rotulo pelo representante do grupo
    numero = {}
    for r in sorted(pai):
        rep = raiz(pai, r)
        if rep not in numero:
            numero[rep] = len(numero) + 1

    for i in range(m):
        for j in range(n):
            if rotulos[i][j] > 0:
                rotulos[i][j] = numero[raiz(pai, int(rotulos[i][j]))]

    return rotulos


def contar(rotulos):
    # quantos objetos a imagem tem
    return int(rotulos.max())


def areas(rotulos):
    # quantos pixels cada objeto tem
    total = contar(rotulos)
    conta = [0] * (total + 1)
    m, n = rotulos.shape
    for i in range(m):
        for j in range(n):
            conta[rotulos[i][j]] += 1
    return conta[1:]
