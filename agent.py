import time
import numpy as np

class AgenteIA:

    def __init__(self, nivel_dificuldade):
        self.nivel_dificuldade = nivel_dificuldade
        self.nos_avaliados = 0
        self.tempo_maximo = 3.0

    def getMelhorMovimento(self, tabuleiro):
        tempo_inicio = time.time()
        self.nos_avaliados = 0

        if self.nivel_dificuldade == 1:
            profundidade = 3
            melhor_coluna, pontuacao = self._minimaxBasico(tabuleiro, profundidade, True)
        elif self.nivel_dificuldade == 2:
            profundidade = 5
            melhor_coluna, pontuacao = self._minimaxComPoda(tabuleiro, profundidade, -float('inf'), float('inf'), True)
            melhor_coluna, pontuacao = self._buscaComLimiteTempo(tabuleiro, tempo_inicio)

        tempo_gasto = time.time() - tempo_inicio
        return melhor_coluna, pontuacao, tempo_gasto

    def _minimaxBasico(self, tabuleiro, profundidade, maximizando):
        self.nos_avaliados += 1

        vencedor = tabuleiro.getVencedor()
        if vencedor != 0 or profundidade == 0 or tabuleiro.isTabuleiroCompleto():
            return -1, self._avaliarPosicao(tabuleiro)

        movimentos_validos = tabuleiro.getMovimentosValidos()

        if maximizando:
            melhor_pontuacao = -float('inf')
            melhor_coluna = movimentos_validos[0]

            for coluna in movimentos_validos:
                tabuleiro.addPeca(coluna, 2) 
                _, pontuacao = self._minimaxBasico(tabuleiro, profundidade - 1, False)
                tabuleiro.removePeca(coluna)

                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_coluna = coluna

            return melhor_coluna, melhor_pontuacao
        else:
            melhor_pontuacao = float('inf')
            melhor_coluna = movimentos_validos[0]

            for coluna in movimentos_validos:
                tabuleiro.addPeca(coluna, 1) 
                _, pontuacao = self._minimaxBasico(tabuleiro, profundidade - 1, True)
                tabuleiro.removePeca(coluna)

                if pontuacao < melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_coluna = coluna

            return melhor_coluna, melhor_pontuacao

    def _minimaxComPoda(self, tabuleiro, profundidade, alfa, beta, maximizando):
        self.nos_avaliados += 1

        vencedor = tabuleiro.getVencedor()
        if vencedor != 0 or profundidade == 0 or tabuleiro.isTabuleiroCompleto():
            return -1, self._avaliarPosicao(tabuleiro)

        movimentos_validos = tabuleiro.getMovimentosValidos()

        if self.nivel_dificuldade == 3:
            movimentos_validos = self._ordenarMovimentos(tabuleiro, movimentos_validos)

        if maximizando:
            melhor_pontuacao = -float('inf')
            melhor_coluna = movimentos_validos[0]

            for coluna in movimentos_validos:
                tabuleiro.addPeca(coluna, 2)
                _, pontuacao = self._minimaxComPoda(tabuleiro, profundidade - 1, alfa, beta, False)
                tabuleiro.removePeca(coluna)

                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_coluna = coluna

                alfa = max(alfa, pontuacao)
                if beta <= alfa:
                    break

            return melhor_coluna, melhor_pontuacao
        else:
            melhor_pontuacao = float('inf')
            melhor_coluna = movimentos_validos[0]

            for coluna in movimentos_validos:
                tabuleiro.addPeca(coluna, 1)
                _, pontuacao = self._minimaxComPoda(tabuleiro, profundidade - 1, alfa, beta, True)
                tabuleiro.removePeca(coluna)

                if pontuacao < melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_coluna = coluna

                beta = min(beta, pontuacao)
                if beta <= alfa:
                    break

            return melhor_coluna, melhor_pontuacao
 
    def _buscaComLimiteTempo(self, tabuleiro, tempo_inicio):
        melhor_coluna = tabuleiro.getMovimentosValidos()[0]
        melhor_pontuacao = 0

        for profundidade in range(1, 15):
            if time.time() - tempo_inicio > self.tempo_maximo:
                break

            try:
                coluna, pontuacao = self._minimaxComPoda(tabuleiro, profundidade, -float('inf'), float('inf'), True)
                melhor_coluna = coluna
                melhor_pontuacao = pontuacao
            except:
                break

        return melhor_coluna, melhor_pontuacao

    def _ordenarMovimentos(self, tabuleiro, movimentos):
        centro = tabuleiro.colunas // 2
        movimentos_ordenados = []
 
        if centro in movimentos:
            movimentos_ordenados.append(centro)
 
        for distancia in range(1, centro + 1):
            if centro - distancia in movimentos and centro - distancia not in movimentos_ordenados:
                movimentos_ordenados.append(centro - distancia)
            if centro + distancia in movimentos and centro + distancia not in movimentos_ordenados:
                movimentos_ordenados.append(centro + distancia)
 
        return movimentos_ordenados
 
    def _avaliarPosicao(self, tabuleiro):
        if self.nivel_dificuldade == 1:
            return self._avaliacaoIniciante(tabuleiro)
        elif self.nivel_dificuldade == 2:
            return self._avaliacaoIntermediaria(tabuleiro)
        else:
            return self._avaliacaoProfissional(tabuleiro)
 
    def _avaliacaoIniciante(self, tabuleiro):
        vencedor = tabuleiro.getVencedor()
        if vencedor == 2: 
            return 1000
        elif vencedor == 1:
            return -1000
 
        pontuacao = 0
        pontuacao += self._contarJanelas(tabuleiro, 2, 3) * 5  # IA
        pontuacao += self._contarJanelas(tabuleiro, 2, 2) * 2
 
        pontuacao -= self._contarJanelas(tabuleiro, 1, 3) * 5  # Humano
        pontuacao -= self._contarJanelas(tabuleiro, 1, 2) * 2
 
        return pontuacao
 
    def _avaliacaoIntermediaria(self, tabuleiro):
        vencedor = tabuleiro.getVencedor()
        if vencedor == 2:
            return 10000
        elif vencedor == 1:
            return -10000

        pontuacao = 0

        pontuacao += self._contarJanelas(tabuleiro, 2, 3) * 50
        pontuacao += self._contarJanelas(tabuleiro, 2, 2) * 10
        pontuacao += self._contarJanelas(tabuleiro, 2, 1) * 1

        pontuacao -= self._contarJanelas(tabuleiro, 1, 3) * 80
        pontuacao -= self._contarJanelas(tabuleiro, 1, 2) * 15
        pontuacao -= self._contarJanelas(tabuleiro, 1, 1) * 2

        coluna_central = tabuleiro.colunas // 2
        contador_central = sum(1 for linha in range(tabuleiro.linhas) 
                             if tabuleiro.grid[linha][coluna_central] == 2)
        pontuacao += contador_central * 6

        return pontuacao

    def _avaliacaoProfissional(self, tabuleiro):
        vencedor = tabuleiro.getVencedor()
        if vencedor == 2:
            return 100000
        elif vencedor == 1:
            return -100000

        pontuacao = 0

        pontuacao += self._avaliarSequenciasAvancadas(tabuleiro, 2) * 100
        pontuacao -= self._avaliarSequenciasAvancadas(tabuleiro, 1) * 120

        pontuacao += self._avaliarForcaPosicao(tabuleiro, 2) * 10
        pontuacao -= self._avaliarForcaPosicao(tabuleiro, 1) * 12

        pontuacao += self._avaliarAmeacas(tabuleiro, 2) * 1000
        pontuacao -= self._avaliarAmeacas(tabuleiro, 1) * 1200

        return pontuacao

    def _contarJanelas(self, tabuleiro, jogador, tamanho):
        contador = 0
        grid = tabuleiro.grid

        for linha in range(tabuleiro.linhas):
            for coluna in range(tabuleiro.colunas - 3):
                janela = grid[linha, coluna:coluna+4]
                if self._avaliarJanela(janela, jogador, tamanho):
                    contador += 1

        for linha in range(tabuleiro.linhas - 3):
            for coluna in range(tabuleiro.colunas):
                janela = grid[linha:linha+4, coluna]
                if self._avaliarJanela(janela, jogador, tamanho):
                    contador += 1
        for linha in range(tabuleiro.linhas - 3):
            for coluna in range(tabuleiro.colunas - 3):
                janela = [grid[linha+i, coluna+i] for i in range(4)]
                if self._avaliarJanela(janela, jogador, tamanho):
                    contador += 1

                janela = [grid[linha+3-i, coluna+i] for i in range(4)]
                if self._avaliarJanela(janela, jogador, tamanho):
                    contador += 1

        return contador

    def _avaliarJanela(self, janela, jogador, tamanho_alvo):
        janela = np.array(janela)
        contador_jogador = np.sum(janela == jogador)
        contador_vazio = np.sum(janela == 0)
        oponente = 1 if jogador == 2 else 2
        contador_oponente = np.sum(janela == oponente)

        return (contador_jogador == tamanho_alvo and 
                contador_vazio == 4 - tamanho_alvo and 
                contador_oponente == 0)

    def _avaliarSequenciasAvancadas(self, tabuleiro, jogador):
        return (self._contarJanelas(tabuleiro, jogador, 3) * 5 + 
                self._contarJanelas(tabuleiro, jogador, 2) * 2)

    def _avaliarForcaPosicao(self, tabuleiro, jogador):
        pontuacao = 0
        coluna_central = tabuleiro.colunas // 2

        for linha in range(tabuleiro.linhas):
            if tabuleiro.grid[linha][coluna_central] == jogador:
                pontuacao += 3

        return pontuacao

    def _avaliarAmeacas(self, tabuleiro, jogador):
        return self._contarJanelas(tabuleiro, jogador, 3) * 10
