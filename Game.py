"""
    Baseado em: Aprenda a aplicar a inteligencia artificial em seus jogos: Teoria dos Jogos Minimax
    Disponivel em <http://aimotion.blogspot.com/2009/01/aprenda-aplicar-inteligencia-artificial.html>

"""

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
        self.formatState(start_state)
        self.min = 2 if j == 1 else 1
        self.max = j #jogador max - bot

        self.player = j
        self.oponent = 2 if j == 1 else 1
        self.maxDepth = 10


    def formatState(self, start_state):
        state = [[0 for col in range(self.n)] for row in range(self.m)]
        for i in range(len(start_state)):
            state[int(i / self.m)][i % self.m] = start_state[i]

        self.state = state
        for row in self.state:
            print(row)

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
                if col_count >= self.k:
                    return True

                right_diag_count = getRightDiagSequence(state, i, j, player, self.m, self.n)
                if right_diag_count == self.k:
                    return True

                left_diag_count = getLeftDiagSequence(state, i, j, player, self.m)
                if left_diag_count == self.k:
                    return True

    def judge(self, board):
        """
        HEURISTICA

        Verifica o estado final do tabuleiro
        +10 para minha vitoria (meu bot)
        -10 para vitoria do adversario
        0 para empate
        :param board:
        :return:
        """
        utility = 0
        self.oponent = 2 if self.player == 1 else 1

        if self.isPLayerWinner(board, self.player):
            utility += 100
        elif self.isPLayerWinner(board, self.oponent):
            utility -= 1000

        else:
            for i in range(0, self.m):
                for j in range(0, self.n):
                    utility += getRightSequence(board, i, j, self.player, self.n)
                    utility += getBottomSequence(board, i, j, self.player, self.m)
                    utility += getRightDiagSequence(board, i, j, self.player, self.m, self.n)
                    utility += getLeftDiagSequence(board, i, j, self.player, self.m)

                    utility -= 100 * getRightSequence(board, i, j, self.oponent, self.n)
                    utility -= 100 * getBottomSequence(board, i, j, self.oponent, self.m)
                    utility -= 100 * getRightDiagSequence(board, i, j, self.oponent, self.m, self.n)
                    utility -= 100 * getLeftDiagSequence(board, i, j, self.oponent, self.m)

        return utility



    def hasEnded(self, board):
        """
        Checa se o jogo foi finalizado. Isso acontece se um dos jogadores completou uma sequencia
        continua de k simbolos ou se a matriz esta cheia.
        :param board:
        :return:
        """
        valid_actions = self.getValidMoves(board)
        gameover = True
        if len(valid_actions) == 0:
            return gameover

        for i in range(0, self.m):
            for j in range(0, self.n):
                row_count1 = getRightSequence(board, i, j, 1, self.n)
                row_count2 = getRightSequence(board, i, j, 2, self.n)
                if row_count1 == self.k or row_count2 == self.k:
                    return gameover

                col_count1 = getBottomSequence(board, i, j, 1, self.m)
                col_count2 = getBottomSequence(board, i, j, 2, self.m)
                if col_count1 == self.k or col_count2 == self.k:
                    return gameover

                right_diag_count1 = getRightDiagSequence(board, i, j, 1, self.m, self.n)
                right_diag_count2 = getRightDiagSequence(board, i, j, 2, self.m, self.n)
                if right_diag_count1 == self.k or right_diag_count2 == self.k:
                    return gameover

                left_diag_count1 = getLeftDiagSequence(board, i, j, 1, self.m)
                left_diag_count2 = getLeftDiagSequence(board, i, j, 2, self.m)
                if left_diag_count1 == self.k or left_diag_count2 == self.k:
                    return gameover

    def maxValue(self, board, alpha, beta, depth):
        """
        Checa se o jogo foi finalizado (Vitória ou empate) ou se está na profundidade máxima de busca.

        No nível MAX, antes de avaliar a próxima possível jogada e suas respectivas contra-jogadas (sub-árvore),
        o melhor valor (alpha) encontrado é comparado com o valor beta.
        Se o alpha for maior,
            então aborta a busca naquele nó.

        :param board:
        :return: Retorna o número de pontos acumulados pelo bot
        """
        self.player = self.min
        depth += 1
        if self.hasEnded(board) or depth == self.maxDepth:
            return self.judge(board)

        # Obtem todas as possiveis jogadas.
        possible_moves = self.getValidMoves(board)
        # Armazena a jogada que tem o melhor score.
        bestScore = -1000
        for possible_move in possible_moves:
            new_game_state = eval(repr(board))
            # bot joga.
            x, y = possible_move
            new_game_state[x][y] = self.max

            # Obtem o minimo do proximo nivel (MIN).
            score = self.minValue(new_game_state, alpha, beta, depth)
            # Pega o maior score dos piores analisados.
            if score >= bestScore:
                bestScore = score
                alpha = bestScore
            if alpha >= beta:
                return alpha

        return bestScore

    def minValue(self, board, alpha, beta, depth):
        """
        Checa se o jogo foi finalizado (Vitória ou empate) ou se está na profundidade máxima de busca.

        No nível MIN, antes de avaliar a próxima jogada e suas respectivas contra-jogadas (sub-árvore),
        o melhor valor (beta) encontrado é comparado com o valor alpha.
        Se o beta for menor,
            então aborte a busca naquele nó.
        :param board:
        :return: Retorna o número de pontos acumulados pelo jogador

        """

        self.player = self.max
        depth += 1
        if self.hasEnded(board) or depth == self.maxDepth:
            return self.judge(board)

        # Obtem todas as possiveis jogadas.
        possible_moves = self.getValidMoves(board)
        # Armazena a jogada que tem o pior score.
        bestScore = 1000
        for possible_move in possible_moves:
            new_game_state = eval(repr(board))
            # Jogador joga.
            x, y = possible_move
            new_game_state[x][y] = self.min
            # Obtem o maximo do proximo nivel (MAX).
            score = self.maxValue(new_game_state, alpha, beta, depth) #recursividade alternada
            # Pega o menor score dos melhores analisados.
            if score <= bestScore:
                bestScore = score
                beta = bestScore
            if beta <= alpha:
                return beta

        return bestScore

    def botDecision(self):
        """
        Testa todas jogadas possiveis
        Armazena a joga que possui o melhor score
        se possuir mais de uma joga disponivel
            percorre todas as jogadas e obtem o prox nivel: min
            por fim fica com o melhor score dos piores analisados,
            ja q min vai piorar eles.

        :return: uma tupla que representa proxima jogada (x, y)
        """
        possible_moves = self.getValidMoves(self.state)
        if not possible_moves:
            return None
        bestScore = -10000
        alpha = -10000
        beta = 10000
        move = None
        depth = -1
        if len(possible_moves) > 1:
            for possible_move in possible_moves:
                new_game_state = eval(repr(self.state))
                x, y = possible_move
                new_game_state[x][y] = self.max
                score = self.minValue(new_game_state, alpha, beta, depth)
                # Pega o maior score dos piores analisados.
                if score >= bestScore:
                    move = possible_move
                    bestScore = score
                    alpha = bestScore
                if alpha >= beta:
                    break #poda
        else:
            move = possible_moves[0] # apenas 1 jogada

        return move

