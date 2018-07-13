"""
Implementação dos metodos para contagem das sequencias feito com auxilo do algoritmo do Wolgan
Disponivel em <https://github.com/wolganens/minimax-tictactoe/blob/master/Problem.py>
"""

import sys

def usage():
    print('Utilização: python3 {} <linhas> <colunas> <jogador> <n de simbolos para vencer> <config do estado>'.format(sys.argv[0]))

def usageTable(m, n):
    print('O estado do jogo deve ter {} elementos'.format(m * n))


def getRightSequence(state, i, j, player, n):
    """
      HORIZONTAL - LINHA
      Conta quantos simbolos em sequencia apartir da posicao atual

      Se o simbolo na posicao atual é 0 ou não é o do jogador,
      então ele não tem nenhuma sequencia a partir dessa posição

      Começa a contar quantos simbolos o jogador tem a partir da posicao atual

      :param state: estado atual do jogo
      :param i: coordenada x da jogada a ser verificada
      :param j: coordenada y da jogada a ser verificada
      :param player: jogador
      :param n: dimensoes do tabuleiro
      :return: numero de elementos em sequencia
      """
    position_symbol = state[i][j]
    if position_symbol == 0 or position_symbol != player:
        return 0
    count = 1
    col = j + 1
    while (col < n) and state[i][col] == player:
        count += 1
        col += 1

    return count

def getBottomSequence(state, i, j, player, m):
    """
      VERTICAL - COLUNA
      Conta quantos simbolos em sequencia apartir da posicao atual

      Se o simbolo na posicao atual é 0 ou não é o do jogador,
      então ele não tem nenhuma sequencia a partir dessa posição

      Começa a contar quantos simbolos o jogador tem a partir da posicao atual

      :param state: estado atual do jogo
      :param i: coordenada x da jogada a ser verificada
      :param j: coordenada y da jogada a ser verificada
      :param player: jogador
      :param m: dimensoes do tabuleiro
      :return: numero de elementos em sequencia
      """
    position_symbol = state[i][j]
    if position_symbol == 0 or position_symbol != player:
        return 0

    count = 1
    row = i + 1
    while (row < m) and state[row][j] == player:
        count += 1
        row += 1
    return count


def getRightDiagSequence(state, i, j, player, m, n):
    """
    DIAGONAL DA DIREITA
    Conta quantos simbolos em sequencia apartir da posicao atual

    Se o simbolo na posicao atual é 0 ou não é o do jogador,
    então ele não tem nenhuma sequencia a partir dessa posição

    Começa a contar quantos simbolos o jogador tem a partir da posicao atual

    :param state: estado atual do jogo
    :param i: coordenada x da jogada a ser verificada
    :param j: coordenada y da jogada a ser verificada
    :param player: jogador
    :param m: dimensoes do tabuleiro
    :param n: dimensoes do tabuleiro
    :return: numero de elementos em sequencia
    """

    position_symbol = state[i][j]
    if position_symbol == 0 or position_symbol != player:
        return 0
    count = 1
    col = j + 1
    row = i + 1
    while (row < m and col < n) and state[row][col] == player:
        count += 1
        row += 1
        col += 1
    return count

def getLeftDiagSequence(state, i, j, player, m):
    """
    DIAGONAL DA ESQUERDA

    Conta quantos simbolos em sequencia apartir da posicao atual

    Se o simbolo na posicao atual é 0 ou não é o do jogador,
    então ele não tem nenhuma sequencia a partir dessa posição

    Começa a contar quantos simbolos o jogador tem a partir da posicao atual

    :param state: estado atual do jogo
    :param i: coordenada x da jogada a ser verificada
    :param j: coordenada y da jogada a ser verificada
    :param player: jogador
    :param m: dimensoes do tabuleiro

    :return: numero de elementos em sequencia
    """
    position_symbol = state[i][j]
    if position_symbol == 0 or position_symbol != player:
        return 0
    count = 1
    col = j - 1
    row = i + 1

    while (row < m and col >= 0) and state[row][col] == player:
        count += 1
        row += 1
        col -= 1
    return count

def getOpponent(player):
    return 2 if player == 1 else 1
