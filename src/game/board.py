import numpy as np

class Board:
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

    def getVencedor(self):
        g = self.grid
        for p in [1, 2]:
            for linha in g:
                if np.any(np.convolve((linha==p).astype(int), np.ones(4), 'valid') == 4):
                    return p
            for coluna in g.T:
                if np.any(np.convolve((coluna==p).astype(int), np.ones(4), 'valid') == 4):
                    return p
            for k in range(-self.linhas+1, self.colunas):
                diag = g.diagonal(k)
                if len(diag) >= 4 and np.any(np.convolve((diag==p).astype(int), np.ones(4), 'valid') == 4):
                    return p
                adiag = np.fliplr(g).diagonal(k)
                if len(adiag) >= 4 and np.any(np.convolve((adiag==p).astype(int), np.ones(4), 'valid') == 4):
                    return p
        return 0
