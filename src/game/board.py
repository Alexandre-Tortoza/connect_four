import numpy as np

class Board:
    # O tabuleiro deve ter dimensão 6x7
    def __init__(self, linhas=6, colunas=7):
        self.linhas = linhas
        self.colunas = colunas
        self.grid = np.zeros((linhas, colunas))

    def getTabuleiro(self):
        return self.grid

    def addPeca(self, coluna, jogador):
        for linha in range(self.grid.shape[0]-1, -1, -1):
            if self.grid[linha, coluna] == 0:
                self.grid[linha, coluna] = jogador
                return True
        return False

