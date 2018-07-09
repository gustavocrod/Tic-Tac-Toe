import sys
from Game import Game
import time


def main():
    if len(sys.argv) < 5:
        print(
            'Utilização: python3 {} <linhas> <colunas> <jogador> <n de simbolos para vencer> <config do estado>'.format(
                sys.argv[0]))
        sys.exit(-1)

    m = int(sys.argv[1])
    n = int(sys.argv[2])
    j = int(sys.argv[3])
    k = int(sys.argv[4])
    state = [int(pos) for pos in sys.argv[5:]]

    if len(state) != m * n:
        print('O estado do jogo deve ter {} elementos'.format(m * n))
        sys.exit(-1)

    p = Game(m, n, j, k, state)
    print(p.botDecision())

if __name__ == '__main__':
    main()