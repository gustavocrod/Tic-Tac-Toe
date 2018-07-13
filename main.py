"""
 Implementação de MiniMax e Poda Alpha Beta para o problema TicTacToe escalável.

(M x N x k problem).

Matricula: 151151360
    Universidade Federal do Pampa

    Baseado em: Aprenda a aplicar a inteligencia artificial em seus jogos: Teoria dos Jogos Minimax
    Disponivel em <http://aimotion.blogspot.com/2009/01/aprenda-aplicar-inteligencia-artificial.html>

    Baseado em: Tic Tac Toe
    Disponivel em <https://cwoebker.com/posts/tic-tac-toe>

    Baseado no codigo de Paulo Rodrigues
    github: <https://github.com/paulorodriguesxv/FreeCodeCamp/tree/master/TicTacToe>

    Baseado no codigo de Wolgan Ens
    github: <https://github.com/wolganens/minimax-tictactoe>

"""
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