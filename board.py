import numpy as np

class Board:
    """Representa o tabuleiro do Connect Four com 6 linhas e 7 colunas"""

    def __init__(self, linhas=6, colunas=7):
        self.linhas = linhas
        self.colunas = colunas
        self.grid = np.zeros((linhas, colunas), dtype=int)

    def getTabuleiro(self):
        return self.grid.copy()

    def isMovimentoValido(self, coluna):
        return 0 <= coluna < self.colunas and self.grid[0][coluna] == 0

    def addPeca(self, coluna, jogador):
        if not self.isMovimentoValido(coluna):
            return False
        for linha in range(self.linhas - 1, -1, -1):
            if self.grid[linha][coluna] == 0:
                self.grid[linha][coluna] = jogador
                return True
        return False

    def removePeca(self, coluna):
        for linha in range(self.linhas):
            if self.grid[linha][coluna] != 0:
                self.grid[linha][coluna] = 0
                break

    def getMovimentosValidos(self):
        return [c for c in range(self.colunas) if self.isMovimentoValido(c)]

    def isTabuleiroCompleto(self):
        return len(self.getMovimentosValidos()) == 0

    def getVencedor(self):
        for jogador in [1, 2]:
            for linha in range(self.linhas):
                if self._verificaLinha(self.grid[linha], jogador):
                    return jogador
            for coluna in range(self.colunas):
                if self._verificaLinha(self.grid[:, coluna], jogador):
                    return jogador
            for k in range(-self.linhas + 1, self.colunas):
                diag = self.grid.diagonal(k)
                if len(diag) >= 4 and self._verificaLinha(diag, jogador):
                    return jogador
                anti_diag = np.fliplr(self.grid).diagonal(k)
                if len(anti_diag) >= 4 and self._verificaLinha(anti_diag, jogador):
                    return jogador
        return 0

    def _verificaLinha(self, linha, jogador):
        if len(linha) < 4:
            return False
        return np.any(np.convolve((linha == jogador).astype(int), np.ones(4), 'valid') == 4)
