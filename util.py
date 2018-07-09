import sys

def usage():
    print('Utilização: python3 {} <linhas> <colunas> <jogador> <n de simbolos para vencer> <config do estado>'.format(sys.argv[0]))

def usageTable(m, n):
    print('O estado do jogo deve ter {} elementos'.format(m * n))
