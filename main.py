# Programa principal do trabalho de rotulacao
#
# uso:
#   python3 main.py imagem.png        rotula a imagem e salva o resultado
#   python3 main.py imagem.png --8    usa vizinhanca de 8
#   python3 main.py --testes          roda os exemplos da aula

import sys

import numpy as np
from PIL import Image

from rotulacao import areas, binarizar, contar, rotular


# cores usadas para pintar os objetos
CORES = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200),
         (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230),
         (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255)]


def colorir(rotulos):
    # pinta cada objeto de uma cor, fundo fica preto
    m, n = rotulos.shape
    saida = np.zeros((m, n, 3), dtype=np.uint8)
    for i in range(m):
        for j in range(n):
            r = rotulos[i][j]
            if r > 0:
                saida[i][j] = CORES[(r - 1) % len(CORES)]
    return saida


def processar(caminho, conectividade):
    img = np.array(Image.open(caminho))
    binaria = binarizar(img)
    rotulos = rotular(binaria, 255, conectividade)

    print("imagem:", caminho)
    print("conectividade:", conectividade)
    print("objetos encontrados:", contar(rotulos))
    print()
    print("objeto  area")
    for i, a in enumerate(areas(rotulos), start=1):
        print(f"{i:>6}  {a:>4}")

    Image.fromarray(binaria).save("binaria.png")
    Image.fromarray(colorir(rotulos)).save("rotulada.png")
    print("\nsalvo em binaria.png e rotulada.png")


# ---- exemplos usados em aula, para testar ----

EXEMPLO = np.array([
    [1, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1, 1],
])

# resposta da aula: 3 componentes, os dois ultimos rotulos eram equivalentes
RESPOSTA = np.array([
    [1, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 3],
    [0, 0, 0, 0, 0, 3, 3],
    [0, 0, 0, 0, 0, 3, 3],
])

EXERCICIO = np.array([
    [0, 0, 0, 0, 0, 255],
    [0, 255, 255, 0, 0, 0],
    [0, 255, 255, 255, 0, 0],
    [0, 0, 255, 255, 0, 0],
    [0, 0, 255, 0, 0, 255],
    [0, 0, 0, 0, 0, 255],
])


def mostrar(rotulos):
    for linha in rotulos:
        print("   ", " ".join(str(v) for v in linha))


def testes():
    print("Exemplo da aula, 4-conectado:")
    r = rotular(EXEMPLO, 1, 4)
    mostrar(r)
    print("    objetos:", contar(r), "| esperado: 3")
    if np.array_equal(r, RESPOSTA):
        print("    a matriz bateu com a resposta da aula")
    else:
        print("    ERRO: matriz diferente da resposta da aula")

    print("\nExemplo da aula, 8-conectado:")
    r = rotular(EXEMPLO, 1, 8)
    mostrar(r)
    print("    objetos:", contar(r), "| esperado: 1")

    print("\nExercicio 6x6, 4-conectado:")
    r = rotular(EXERCICIO, 255, 4)
    mostrar(r)
    print("    objetos:", contar(r), "| esperado: 3")

    print("\nExercicio 6x6, 8-conectado:")
    r = rotular(EXERCICIO, 255, 8)
    mostrar(r)
    print("    objetos:", contar(r), "| esperado: 3")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python3 main.py imagem.png")
        print("     python3 main.py imagem.png --8")
        print("     python3 main.py --testes")
    elif sys.argv[1] == "--testes":
        testes()
    else:
        conectividade = 8 if "--8" in sys.argv else 4
        processar(sys.argv[1], conectividade)
