import sys
from Problem import Problem
import time


def main():
    if len(sys.argv) < 5:
        print(
            'Utilização: python3 {} <linhas> <colunas> <jogador> <n de simbolos para vencer> <config do estado>'.format(
                sys.argv[0]))
        sys.exit(-1)

    m = int(sys.argv[1])
    n = int(sys.argv[2])
    player_index = int(sys.argv[3])
    symbols_count = int(sys.argv[4])
    start_state = [int(pos) for pos in sys.argv[5:]]

    if len(start_state) != m * n:
        print('O estado do jogo deve ter {} elementos'.format(m * n))
        sys.exit(-1)

    p = Problem(m, n, player_index, symbols_count, start_state)
    next_action = p.get_action(p.start_state, 15 if m * n < 12 else symbols_count + 5)
    print(next_action[2])


if __name__ == '__main__':
    main()