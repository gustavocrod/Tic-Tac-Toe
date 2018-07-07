from random import randrange
import copy


class Problem(object):
    """Classe principal para o problema do jogo"""

    def __init__(self, m, n, player_index, symbols_count, start_state):
        # Número de linhas
        self.m = m
        # Número de colunas
        self.n = n
        self.current_player = player_index
        # Indices dos jogadores
        self.max_player = player_index
        self.min_player = 2 if player_index == 1 else 1
        # Número de simbolos em sequencia para uma vitória
        self.symbols_count = symbols_count
        # Profundidade máxima que a busca na árvore pode expandir
        self.max_depth = 10
        # Configuração inicial do "tabuleiro"
        self.format_state(start_state)

    def format_state(self, start_state):
        state = [[0 for col in range(self.n)] for row in range(self.m)]
        for i in range(len(start_state)):
            state[int(i / self.m)][i % self.m] = start_state[i]

        self.start_state = [0, state, None]

    # Printa no saida do so a configuração do tabuleiro
    def print_state(self, state):
        for i in range(self.m):
            print('-'.join(['-----' for k in range(self.n)]))
            print(' '.join(['| X |' if state[1][i][j] == 1 else '| O |' if state[1][i][j] == 2  else '|   |' for j in
                            range(self.n)]))
        print('-'.join(['-----' for k in range(self.n)]))

    # Conta quantos simbolos em sequencia (na linha) o jogador tem na posição atual
    def get_right_seq(self, state, i, j, player):
        # Qual indice esta na posição atual a ser verificada
        position_symbol = state[1][i][j]
        # Se o simbolo na posicao atual é 0 ou não é o do jogador,
        # então ele não tem nenhuma sequencia a partir dessa posição
        if position_symbol == 0 or position_symbol != player:
            return 0
        # Começa a contar quantos simbolos o jogador tem a partir da posicao atual		
        count = 1
        col = j + 1
        # Enquanto os proximos simbolos forem do jogador e não passar do limite, contabiliza
        # os simbolos
        while col < self.n and state[1][i][col] == player:
            count += 1
            col += 1
        return count

    # Conta quantos simbolos em sequencia (na coluna) o jogador tem na posição atual
    def get_bottom_seq(self, state, i, j, player):
        # Qual indice esta na posição atual a ser verificada
        position_symbol = state[1][i][j]
        # Se o simbolo na posicao atual é 0 ou não é o do jogador,
        # então ele não tem nenhuma sequencia a partir dessa posição
        if position_symbol == 0 or position_symbol != player:
            return 0
        # Começa a contar quantos simbolos o jogador tem a partir da posicao atual		
        count = 1
        row = i + 1
        # Enquanto os proximos simbolos forem do jogador e não passar do limite, contabiliza
        # os simbolos
        while row < self.m and state[1][row][j] == player:
            count += 1
            row += 1
        return count

    # Conta quantos simbolos em sequencia (na diagonal da direita) o jogador tem na posição atual
    def get_right_diag_seq(self, state, i, j, player):
        # Qual indice esta na posição atual a ser verificada
        position_symbol = state[1][i][j]
        # Se o simbolo na posicao atual é 0 ou não é o do jogador,
        # então ele não tem nenhuma sequencia a partir dessa posição
        if position_symbol == 0 or position_symbol != player:
            return 0
        # Começa a contar quantos simbolos o jogador tem a partir da posicao atual		
        count = 1
        col = j + 1
        row = i + 1
        # Enquanto os proximos simbolos forem do jogador e não passar do limite, contabiliza
        # os simbolos
        while (row < self.m and col < self.n) and state[1][row][col] == player:
            count += 1
            row += 1
            col += 1
        return count

    # Conta quantos simbolos em sequencia (na diagonal da direita) o jogador tem na posição atual
    def get_left_diag_seq(self, state, i, j, player):
        # Qual indice esta na posição atual a ser verificada
        position_symbol = state[1][i][j]
        # Se o simbolo na posicao atual é 0 ou não é o do jogador,
        # então ele não tem nenhuma sequencia a partir dessa posição
        if position_symbol == 0 or position_symbol != player:
            return 0
        # Começa a contar quantos simbolos o jogador tem a partir da posicao atual		
        count = 1
        col = j - 1
        row = i + 1
        # Enquanto os proximos simbolos forem do jogador e não passar do limite, contabiliza
        # os simbolos
        while (row < self.m and col >= 0) and state[1][row][col] == player:
            count += 1
            row += 1
            col -= 1
        return count

    def is_player_winner(self, state, player):
        for i in range(0, self.m):
            for j in range(0, self.n):
                row_count1 = self.get_right_seq(state, i, j, player)
                if row_count1 == self.symbols_count:
                    return True

                col_count1 = self.get_bottom_seq(state, i, j, player)
                if col_count1 >= self.symbols_count:
                    return True

                right_diag_count1 = self.get_right_diag_seq(state, i, j, player)
                if right_diag_count1 == self.symbols_count:
                    return True

                left_diag_count1 = self.get_left_diag_seq(state, i, j, player)
                if left_diag_count1 == self.symbols_count:
                    return True

    # Determinina se as posições atuais no tabuleiro configuram alguma vitória
    def terminal_test(self, state):
        # Se não há mais sucessores
        if len(self.get_valid_actions(state)) == 0:
            return True
        for i in range(0, self.m):
            for j in range(0, self.n):
                row_count1 = self.get_right_seq(state, i, j, 1)
                row_count2 = self.get_right_seq(state, i, j, 2)
                if row_count1 == self.symbols_count or row_count2 == self.symbols_count:
                    return True

                col_count1 = self.get_bottom_seq(state, i, j, 1)
                col_count2 = self.get_bottom_seq(state, i, j, 2)
                if col_count1 == self.symbols_count or col_count2 == self.symbols_count:
                    return True

                right_diag_count1 = self.get_right_diag_seq(state, i, j, 1)
                right_diag_count2 = self.get_right_diag_seq(state, i, j, 2)
                if right_diag_count1 == self.symbols_count or right_diag_count2 == self.symbols_count:
                    return True

                left_diag_count1 = self.get_left_diag_seq(state, i, j, 1)
                left_diag_count2 = self.get_left_diag_seq(state, i, j, 2)
                if left_diag_count1 == self.symbols_count or left_diag_count2 == self.symbols_count:
                    return True

    def player_symbols_in_row(self, state):
        player_row_count = list()
        for i in range(self.m):
            player_one = [j for j in range(self.n) if state[i][j] == 1]
            player_two = [j for j in range(self.n) if state[i][j] == 2]
            player_row_count.append([player_one, player_two])
        return player_row_count

    # Função heurística para atribuir um valor a um estado
    def h(self, state):
        utility = 0
        opponent = 2 if self.current_player == 1 else 1
        if self.is_player_winner(state, self.current_player):
            utility += 100
        if self.is_player_winner(state, opponent):
            utility -= 10000
        for i in range(0, self.m):
            for j in range(0, self.n):
                utility += self.get_right_seq(state, i, j, self.current_player)
                utility += self.get_bottom_seq(state, i, j, self.current_player)
                utility += self.get_right_diag_seq(state, i, j, self.current_player)
                utility += self.get_left_diag_seq(state, i, j, self.current_player)

                utility -= 100 * self.get_right_seq(state, i, j, opponent)
                utility -= 100 * self.get_bottom_seq(state, i, j, opponent)
                utility -= 100 * self.get_right_diag_seq(state, i, j, opponent)
                utility -= 100 * self.get_left_diag_seq(state, i, j, opponent)
        return utility

    def get_valid_actions(self, state):
        actions = [[i, j] for i in [i for i in range(self.m)] for j in range(self.n) if state[1][i][j] == 0]
        return actions

    def get_successor(self, state, action, player):
        state_copy = copy.deepcopy(state)
        i, j = action
        state_copy[0] = None
        state_copy[1][i][j] = player
        state_copy[2] = '{} {}'.format(i, j)
        return state_copy

    def get_action(self, state, depth):
        alpha = [-99999999]
        beta = [99999999]
        val = self.value(state, depth, alpha, beta, True)
        return val

    def value(self, state, depth, alpha, beta, max_turn):
        if depth == 0 or self.terminal_test(state):
            state[0] = self.h(state)
            return state

        if max_turn:
            self.current_player = self.min_player
            return self.max_value(state, depth, alpha, beta)
        else:
            self.current_player = self.max_player
            return self.min_value(state, depth, alpha, beta)

    def max_value(self, state, depth, alpha, beta):
        v = [-999999999]
        sucessors = [self.get_successor(state, action, self.max_player) for action in self.get_valid_actions(state)]
        for s in sucessors:
            v = max(v, self.value(s, depth - 1, alpha, beta, False))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v

    def min_value(self, state, depth, alpha, beta):
        v = [999999999]
        sucessors = [self.get_successor(state, action, self.min_player) for action in self.get_valid_actions(state)]
        for s in sucessors:
            v = min(v, self.value(s, depth - 1, alpha, beta, True))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v