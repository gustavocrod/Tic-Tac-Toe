import math
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
        self.moveChoice = None # jogada
        self.maxDepth = 6 # profundidade maxima
        self.baseScore = 0 # score base


    def formatState(self, start_state):
        state = [[0 for col in range(self.n)] for row in range(self.m)]
        for i in range(len(start_state)):
            state[int(i / self.m)][i % self.m] = start_state[i]

        self.state = state

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
        """

        :param candidate_moves: lista com os possiveis movimentos
        :return: melhor jogada
        """
        max = -1000
        best_move = list()
        for node in candidate_moves:
            if node["val"] > max:
                max = node["val"]
                best_move = node["move"]
        return best_move

    def evaluateState(self, state, depth):
        """
        HEURISTICA estado nao-final - Ajuda do Wolgan

        :param state:
        :param depth:
        :return: retorna o score base - profundidade, se ganhou
                 retorna profundidade - score base, se perdeu
                 retorna 0 se empatou
                 retorna uma pontuação com base no tamanho da sequencia do jogador com maior sequencia, se nao chegou a estado terminal
        """
        if self.isPLayerWinner(state, self.max): # ganha
            return self.baseScore - depth
        elif self.isPLayerWinner(state, self.min): # perde
            return depth - self.baseScore
        elif len(self.getValidMoves(state)) == 0: # empate
            return 0

        else:
            sequence_count = list()
            for i in range(0, self.m):
                for j in range(0, self.n): # Heuristica construida com a ajuda do Wolgan
                    sequence_count.append(getRightSequence(state, i, j, self.max, self.n)),
                    sequence_count.append(getBottomSequence(state, i, j, self.max, self.m)),
                    sequence_count.append(getRightDiagSequence(state, i, j, self.max, self.m, self.n)),
                    sequence_count.append(getLeftDiagSequence(state, i, j, self.max, self.m))

                    sequence_count.append(-1 * (getRightSequence(state, i, j, self.min, self.n) * 3)),
                    sequence_count.append(-1 * (getBottomSequence(state, i, j, self.min, self.m) * 3)),
                    sequence_count.append(-1 * (getRightDiagSequence(state, i, j, self.min, self.m, self.n) * 3)),
                    sequence_count.append(-1 * (getLeftDiagSequence(state, i, j, self.min, self.m) * 3))

            return max(sequence_count, key=lambda x: abs(x))

    def terminalState(self, state, player, depth):
        """
        :param state: estado atual
        :param player: jogador atual
        :param depth: profundidade atual
        :return: retorna true se tem um vencedor, se empatou ou se chegou numa profundidade maxima
        """
        if len(self.getValidMoves(state)) == 0:
            return True

        if self.isPLayerWinner(state, getOpponent(player)) or self.isPLayerWinner(state, player) or depth == self.maxDepth:
            return True

    def isMaxTurn(self, player):
        """
        Retorna se eh a vez do max jogar
        :param player:
        :return:
        """
        return player == self.max

    def alphabeta(self, state, player, alpha, beta, depth):
        """
        Testa todas jogadas possiveis
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
            return self.evaluateState(state, depth) # retorna o melhor estado da proxima jogada

        for move in valid_moves:
            next_move = self.makeMove(state, move, player)
            if self.isMaxTurn(player): # se for jogada do max
                val = max(val, self.alphabeta(next_move, getOpponent(player), alpha, beta, depth + 1)) # melhor valor de min
            else: # se for jogada de min
                val = min(val, self.alphabeta(next_move, getOpponent(player), alpha, beta, depth + 1)) # pior valor de max

            if self.isMaxTurn(player): # se for a jogada de max
                alpha = max(val, alpha)
                if alpha >= beta: # se alpha for melhor q beta
                    break #poda pois ele vai jogar a melhor
            else: # jogada de min
                beta = min(val, beta)
                if beta < alpha: # se beta pior q alpha
                    break #poda pois ele vai jogar a pior
        return val # retorna o melhor valor. Min = pior, Max = maior

    def botDecision(self):
        """
        Começa a primeira jogada como max
        vai adicionando as jogadas em uma lista de possiveis jogadas.
        Faz a possivel jogada
        val recebe o valor de alpha beta,
        armazena o melhor val de todas as melhores jogadas
        armazena essas melhores jogadas
        Escolhe a jogada de melhor custo


        :return: uma tupla que representa proxima jogada (x, y)
        """
        possible_moves = self.getValidMoves(self.state)
        self.baseScore = len(possible_moves) + 1 # score base eh quantas jogadas ele pode jogar + 1
        if not possible_moves:
            return None

        if len(possible_moves) == self.m * self.n:
           return (math.floor(self.m/2), math.floor(self.n/2)) # retorna o meio - estatisticamente melhor

        a = -99999
        alpha = -99999
        beta = 9999999
        depth = 0
        choices = []
        if len(possible_moves) > 1:
            for possible_move in possible_moves:
                new_game_state = self.makeMove(self.state, possible_move, self.max)
                val = self.alphabeta(new_game_state, self.min, alpha, beta, depth) # jogada do min
                node = {"val": val, "move": possible_move} # armazena o a melhor jogada

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

