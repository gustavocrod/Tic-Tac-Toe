"""
    Baseado em: Aprenda a aplicar a inteligencia artificial em seus jogos: Teoria dos Jogos Minimax
    Disponivel em <http://aimotion.blogspot.com/2009/01/aprenda-aplicar-inteligencia-artificial.html>

"""

import numpy as np

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
        self.bot = j
        self.player = 2 if j == 1 else 1
        self.maxDepth = 3


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

    def calculateChances(self, board, turn):
        """
        dado o tabuleiro suposto, calcula quantas chances
        o jogador selecionado ainda tem para ganhar e retorna o seu valor
        :param board:
        :param turn:
        :return:
        """
        winning_rows = eval(repr(self.getEndGameStates()))
        for i in range(self.m):
            for j in range(self.n):
                if board[i][j] != 0 and board[i][j] != turn:
                    forbidden_play = (i, j)
                    list_remove = list()
                    for row in winning_rows:
                        if forbidden_play in row:
                            list_remove.append(row)
                    for chance in list_remove:
                        winning_rows.remove(chance)

        return len(winning_rows)

    def judge(self, board):
        """
        Verifica o estado final do tabuleiro
        +10 para minha vitoria (meu bot)
        -10 para vitoria do adversario
        0 para empate
        :param board:
        :return:
        """
        winning_rows = list(self.getEndGameStates())

        winner = None
        for row in winning_rows:
            row_win = [board[x][y] for x, y in row]
            if row_win == [1, 1, 1]:
                winner = 1
                break
            elif row_win == [2, 2, 2]:
                winner = 2
                break
        if winner == self.bot:
            return 10
        if winner == None: #empate
            if self.hasEnded(board):
                return 0
            else: #calcula as chances que o jogador da jogada ainda tem pra ganhar
                return self.calculateChances(board, self.bot) - self.calculateChances(board, self.player)
        return -10

    def hasEnded(self, board):
        """
        Checa se o jogo foi finalizado. Isso acontece se um dos jogadores completou uma sequencia
        continua de k simbolos ou se a matriz esta cheia.
        :param board:
        :return:
        """
        winning_rows = list(self.getEndGameStates())
        gameover = True
        for i in range(self.m):
            for j in range(self.n):
                if (board[i][j] == 0):
                    gameover = False
        for row in winning_rows:
            row_winner = [board[x][y] for x, y in row]

            if row_winner == [1, 1, 1] or row_winner == [2, 2, 2]:
                gameover = True
                break
        return gameover

    def getEndGameStates(self):
        """
        Gera todas as combinacoes possiveis de K simbolos que ganham o jogo
        (setado para 3x3 por hora)

        :return:uma matriz contendo as tuplas(coordenadas) das configuracoes vencedoras
        """
        end_state = [[(0, 0), (0, 1), (0, 2)],
                     [(1, 0), (1, 1), (1, 2)],
                     [(2, 0), (2, 1), (2, 2)],
                     [(0, 0), (1, 0), (2, 0)],
                     [(0, 1), (1, 1), (2, 1)],
                     [(0, 2), (1, 2), (2, 2)],
                     [(0, 0), (1, 1), (2, 2)],
                     [(0, 2), (1, 1), (2, 0)]]

        return end_state

    def maxValue(self, board, alpha, beta, depth):
        """
        Checa se o jogo foi finalizado (Vitória ou empate) ou se está na profundidade máxima de busca.

        No nível MAX, antes de avaliar a próxima possível jogada e suas respectivas contra-jogadas (sub-árvore),
        o melhor valor (alpha) encontrado é comparado com o valor beta.
        Se o alpha for maior,
            então aborta a busca naquele nó.

        :param board:
        :return: Retorna o número de pontos acumulados pelo bot - número de pontos acumulados pelo outro jogador

        """
        depth += 1
        if self.hasEnded(board) or depth == self.maxDepth:
            return self.judge(board)

        # Obtem todas as possiveis jogadas.
        possible_moves = self.getValidMoves(board)
        # Armazena a jogada que tem o melhor score.
        bestScore = -100
        for possible_move in possible_moves:
            new_game_state = eval(repr(board))
            # bot joga.
            x, y = possible_move
            new_game_state[x][y] = self.bot
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
        :return: Retorna o número de pontos acumulados pelo jogador - número de pontos acumulados pelo outro jogador

        """
        depth += 1
        if self.hasEnded(board) or depth == self.maxDepth:
            return self.judge(board)

        # Obtem todas as possiveis jogadas.
        possible_moves = self.getValidMoves(board)
        # Armazena a jogada que tem o pior score.
        bestScore = 100
        for possible_move in possible_moves:
            new_game_state = eval(repr(board))
            # Jogador joga.
            x, y = possible_move
            new_game_state[x][y] = self.player
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
        bestScore = -100
        alpha = -100
        beta = 100
        move = None
        depth = -1
        if len(possible_moves) > 1:
            for possible_move in possible_moves:
                new_game_state = eval(repr(self.state))
                x, y = possible_move
                new_game_state[x][y] = self.bot
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

