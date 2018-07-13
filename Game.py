"""
    Baseado em: Aprenda a aplicar a inteligencia artificial em seus jogos: Teoria dos Jogos Minimax
    Disponivel em <http://aimotion.blogspot.com/2009/01/aprenda-aplicar-inteligencia-artificial.html>

"""
import os
import math
import random
from util import *

class Game:
    """

        0 se o quadrado estiver vazio, 1 se o quadrado for ocupado por uma jogada do "X"
        e 2 se o quadrado for ocupado por uma jogada do "O".

    """
    def __init__(self, m, n, j, k, start_state):
        """
        :param m: numero de linhas
        :param n: numero de colunas
        :param j: o jogador
        :param k: numero elementos necessarios em uma fileira para ganhar o jogo
        :param state: um estado do jogo Tic-tac-toe
        """
        self.m = m
        self.n = n
        self.k = k
        self.min = 2 if j == 1 else 1
        self.max = j  # jogador max - bot

        self.formatState(start_state)
        self.moveChoice = None
        self.player = j
        self.maxDepth = 15
        self.baseScore = 0


    def formatState(self, start_state):
        state = [[0 for col in range(self.n)] for row in range(self.m)]
        for i in range(len(start_state)):
            state[int(i / self.m)][i % self.m] = start_state[i]

        #print("player", self.max)

        print("Initial state:")
        self.state = state
        for row in self.state:
            print(row)
        #input()
        #os.system("clear")

    def getValidMoves(self, board):
        """
        Analista o tabuleiro
        :param board:
        :return: retorna as posicoes que ainda estao vazias
        """

        possible_moves = list()
        for i in range(self.m):
            for j in range(self.n):
                if board[i][j] == 0:
                    possible_moves.append((i, j))
        return possible_moves


    def isPLayerWinner(self, state, player):
        """
        Testa se o "player" eh o vencedor - current player
        :param state:
        :param player:
        :return:
        """

        for i in range(0, self.m):
            for j in range(0, self.n):
                row_count = getRightSequence(state, i, j, player, self.n)
                if row_count == self.k:
                    return True

                col_count = getBottomSequence(state, i, j, player, self.m)
                if col_count == self.k:
                    return True

                right_diag_count = getRightDiagSequence(state, i, j, player, self.m, self.n)
                if right_diag_count == self.k:
                    return True

                left_diag_count = getLeftDiagSequence(state, i, j, player, self.m)
                if left_diag_count == self.k:
                    return True

        return False

    def makeMove(self, state, move, player):
        x, y = move
        new_game_state = eval(repr(state))
        new_game_state[x][y] = player
        return new_game_state

    def getScore(self, candidate_moves):
        max = -1000
        best_move = list()
        for node in candidate_moves:
            if node["val"] > max:
                max = node["val"]
                best_move = node["move"]
        return best_move

    def evaluateState(self, state, depth):
        if self.isPLayerWinner(state, self.max):
            return self.baseScore - depth
        elif self.isPLayerWinner(state, self.min):
            return depth - self.baseScore
        else:
            return 0

    def terminalState(self, state, player, depth):
        if len(self.getValidMoves(state)) == 0:
            return True

        if self.isPLayerWinner(state, getOpponent(player)) or self.isPLayerWinner(state, player) or depth == self.maxDepth:
            return True

    def isMaxTurn(self, player):
        return player == self.max

    def alphabeta(self, state, player, alpha, beta, depth):

        """

        Testa todas jogadas possiveis
        Armazena a jogada que possui o melhor score
        se possuir mais de uma jogada disponivel
        percorre todas as jogadas e obtem o prox nivel: min
        por fim fica com o melhor score dos piores analisados,
        ja q min vai piorar eles.

        Recursivamente, chama alphabeta para todos os movimentos possiveis
        Se for a jogada do bot, retorna o maior resultado, senao o menor (minimax)

        para se tem algum vencedor, ou se chegou em maxDepth
        :param player: jogador da vez
        :param state: o estado atual do jogo
        :param alpha:
        :param beta:
        :return:
        """
        valid_moves = self.getValidMoves(state)

        if self.isMaxTurn(player):
            val = -99999
        else:
            val = 99999

        if self.terminalState(state, player, depth):
            return self.evaluateState(state, depth)

        for move in valid_moves:
            next_move = self.makeMove(state, move, player)
            if self.isMaxTurn(player):
                val = max(val, self.alphabeta(next_move, getOpponent(player), alpha, beta, depth + 1))
            else:
                val = min(val, self.alphabeta(next_move, getOpponent(player), alpha, beta, depth + 1))

            if self.isMaxTurn(player):
                alpha = max(val, alpha)
                if alpha >= beta:
                    break
            else:
                beta = min(val, beta)
                if beta < alpha:
                    break #poda
        return val

    def botDecision(self):
        """
        Definicao algoritmica:
            Se o jogo acabou, retorne a pontuação da perspectiva de “max”
            Do contrário, obtenha uma lista de novos estados de jogo para todos os possíveis movimentos.
            Cria uma lista de pontuação
            Para cada um desses estados, adicione o resultado minimax que resulta a lista de pontuação
            Se for a vez de “max” jogar, retorne a maior pontuação da lista de resultados
            Se for a vez de “min” jogar, retorne a menor pontuação da lista de resultados

        :return: uma tupla que representa proxima jogada (x, y)
        """
        possible_moves = self.getValidMoves(self.state)
        self.baseScore = len(possible_moves)+1
        if not possible_moves:
            return None

        if len(possible_moves) == self.m * self.n:
            return (math.floor(self.m/2), math.floor(self.n/2)) # retorna o meio - estatisticamente melhor

        a = -20
        alpha = -20
        beta = 20
        depth = 0
        choices = []
        if len(possible_moves) > 1:
            for possible_move in possible_moves:
                new_game_state = self.makeMove(self.state, possible_move, self.max)
                val = self.alphabeta(new_game_state, getOpponent(self.player), alpha, beta, depth)

                node = {"val": val, "move": possible_move}

                if val > a:
                    a = val
                    choices = [node]
                elif val == a:
                    choices.append(node)
        else:
            self.moveChoice = [possible_moves[0]] # apenas 1 jogada
            return self.moveChoice[0]

        self.moveChoice = self.getScore(choices)
        return self.moveChoice

