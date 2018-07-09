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


    def formatState(self, start_state):
        state = [[0 for col in range(self.n)] for row in range(self.m)]
        for i in range(len(start_state)):
            state[int(i / self.m)][i % self.m] = start_state[i]

        self.state = [0, state, None]

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

    def judge(self, board):
        """
        Verifica o estado final do tabuleiro
        +1 para minha vitoria (meu bot)
        -1 para vitoria do adversario
        0 para empate
        :param board:
        :return:
        """
        winning_rows = list(self.getEndGameStates())
        winner = None
        for row in winning_rows:
            row_win = [board[x][y] for x, y in row]
            if sum(row_win) == self.k:
                winner = 1
                break
            elif sum(row_win) == 2 * self.k:
                winner = 2
                break
        if winner == self.bot:
            return 1
        if winner == None:
            return 0
        return -1

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
                if (board[i - 1][j - 1] == 0):
                    gameover = False
        for row in winning_rows:
            row_winner = [board[x][y] for x, y in row]
            if sum(row_winner) == self.k or sum(row_winner) == 2 * self.k:
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

    def maxValue(self, board):
        """
        Checka se o jogo foi finalizado (vitoria ou empate)
        :param board:
        :return: +1 para vitoria do bot
                 -1 para adversario
                 0 para empate
        """
        if self.hasEnded(board):
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
            score = self.minValue(new_game_state)
            # Pega o maior score dos piores analisados.
            if score >= bestScore:
                bestScore = score

        return bestScore

    def minValue(self, board):
        """
        Checka se o jogo foi finalizado (vitoria ou empate)
        :param board:
        :return: +1 para vitoria do bot
                 -1 para adversario
                 0 para empate
        """
        if self.hasEnded(board):
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
            score = self.maxValue(new_game_state) #recursividade alternada
            # Pega o menor score dos melhores analisados.
            if score <= bestScore:
                bestScore = score

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
        bestScore = -100

        if len(possible_moves) > 1:
            for possible_move in possible_moves:
                new_game_state = eval(repr(self.state))

                px, py = possible_move
                new_game_state[px][py] = 1
                score = self.minValue(new_game_state)
                # Pega o maior score dos piores analisados.
                if score >= bestScore:
                    move = possible_move
                    bestScore = score
        else:
            # Apenas uma única jogada, esta será a jogada do bot.
            move = possible_moves[0]

        return move
