import sys
from Game import Game
from util import *



def main():
    if len(sys.argv) < 5:
        usage()
        sys.exit(-1)

    m = int(sys.argv[1])
    n = int(sys.argv[2])
    j = int(sys.argv[3])
    k = int(sys.argv[4])
    state = [int(pos) for pos in sys.argv[5:]]

    if len(state) != m * n:
        usageTable(m, n)
        sys.exit(-1)

    p = Game(m, n, j, k, state)
    decision = p.botDecision()
    if decision:
        print(decision[0], decision[1])
    else:
        print("Fim de jogo!")

if __name__ == '__main__':
    main()