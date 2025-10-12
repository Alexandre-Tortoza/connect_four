import numpy as np

class Board:
    """
    Classe responsável por representar e manipular o tabuleiro do jogo.

    O tabuleiro é uma matriz 6x7 (por padrão), onde:
        - 0 representa uma célula vazia
        - 1 representa uma peça do jogador
        - 2 representa uma peça da Maquina
    """

    def __init__(self, linhas=6, colunas=7):
        """
        Inicializa o tabuleiro com o número especificado de linhas e colunas.

        Args:
            linhas (int): número de linhas do tabuleiro (padrão: 6)
            colunas (int): número de colunas do tabuleiro (padrão: 7)
        """
        self.linhas = linhas
        self.colunas = colunas
        self.grid = np.zeros((linhas, colunas), dtype=int)

    def getTabuleiro(self):
        """
        Retorna uma cópia do estado atual do tabuleiro.

        Returns:
            numpy.ndarray: matriz representando o estado atual do tabuleiro
        """
        return self.grid.copy()

    def isMovimentoValido(self, coluna):
        """
        Verifica se uma jogada em uma coluna é válida.

        Args:
            coluna (int): índice da coluna a verificar

        Returns:
            bool: True se o movimento é válido (coluna existe e não está cheia), False caso contrário
        """
        return 0 <= coluna < self.colunas and self.grid[0][coluna] == 0

    def addPeca(self, coluna, jogador):
        """
        Adiciona uma peça do jogador especificado na coluna informada.

        Args:
            coluna (int): índice da coluna onde a peça será colocada
            jogador (int): identificador do jogador (1 = humano, 2 = IA)

        Returns:
            bool: True se a peça foi colocada com sucesso, False se o movimento for inválido
        """
        if not self.isMovimentoValido(coluna):
            return False
        for linha in range(self.linhas - 1, -1, -1):
            if self.grid[linha][coluna] == 0:
                self.grid[linha][coluna] = jogador
                return True
        return False

    def removePeca(self, coluna):
        """
        Remove a peça mais alta (primeira de cima para baixo) da coluna especificada.

        Args:
            coluna (int): índice da coluna
        """
        for linha in range(self.linhas):
            if self.grid[linha][coluna] != 0:
                self.grid[linha][coluna] = 0
                break

    def getMovimentosValidos(self):
        """
        Retorna uma lista com todas as colunas válidas para jogada.

        Returns:
            list[int]: índices das colunas válidas
        """
        return [c for c in range(self.colunas) if self.isMovimentoValido(c)]

    def isTabuleiroCompleto(self):
        """
        Verifica se o tabuleiro está completamente cheio.

        Returns:
            bool: True se não há mais movimentos válidos, False caso contrário
        """
        return len(self.getMovimentosValidos()) == 0

    def getVencedor(self):
        """
        Determina se há um vencedor no tabuleiro.

        Retorna:
            0: se não houver vencedor
            1: se o jogador venceu
            2: se a Maquina venceu

        Returns:
            int: identificador do vencedor (0, 1 ou 2)
        """
        for jogador in [1, 2]:
            for linha in range(self.linhas):
                if self.verificaLinha(self.grid[linha], jogador):
                    return jogador
            for coluna in range(self.colunas):
                if self.verificaLinha(self.grid[:, coluna], jogador):
                    return jogador
            for k in range(-self.linhas + 1, self.colunas):
                diag = self.grid.diagonal(k)
                if len(diag) >= 4 and self.verificaLinha(diag, jogador):
                    return jogador
                anti_diag = np.fliplr(self.grid).diagonal(k)
                if len(anti_diag) >= 4 and self.verificaLinha(anti_diag, jogador):
                    return jogador
        return 0

    def verificaLinha(self, linha, jogador):
        """
        Verifica se há uma sequência de quatro peças consecutivas do mesmo jogador.

        Args:
            linha (numpy.ndarray): vetor representando uma linha, coluna ou diagonal
            jogador (int): identificador do jogador (1 ou 2)

        Returns:
            bool: True se há quatro peças consecutivas do jogador, False caso contrário
        """
        if len(linha) < 4:
            return False
        return np.any(np.convolve((linha == jogador).astype(int), np.ones(4), 'valid') == 4)
