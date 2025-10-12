import time
import numpy as np

class AgenteIA:
    """
    Classe responsável pela lógica da Maquina.

    A Maquina usa o algoritmo Minimax com variações:
        1. Iniciante  -> Minimax básico
        2. Intermediário -> Minimax com poda alfa-beta e limite de tempo
        3. Profissional  -> Poda + heurísticas avançadas de avaliação
    """

    def __init__(self, nivel_dificuldade):
        """
        Inicializa Maquina com o nível de dificuldade escolhido.

        Args:
            nivel_dificuldade (int): 1 = Iniciante, 2 = Intermediário, 3 = Profissional
        """
        self.nivel_dificuldade = nivel_dificuldade
        self.nos_avaliados = 0
        self.tempo_maximo = 3.0

    # ============================================================
    # FUNÇÕES PRINCIPAIS DE DECISÃO
    # ============================================================

    def getMelhorJogada(self, tabuleiro):
        """
        Determina a melhor jogada possível para o estado atual do tabuleiro.

        A lógica varia conforme a dificuldade:
            - Nível 1: Minimax básico (profundidade fixa)
            - Nível 2: Minimax com poda alfa-beta + busca limitada por tempo

        Args:
            tabuleiro (Board): instância do tabuleiro atual

        Returns:
            tuple[int, float, float]: (coluna escolhida, pontuação da jogada, tempo gasto)
        """
        tempo_inicio = time.time()
        self.nos_avaliados = 0

        if self.nivel_dificuldade == 1:
            profundidade = 3
            melhor_coluna, pontuacao = self.minimaxBasico(tabuleiro, profundidade, True)
        elif self.nivel_dificuldade == 2:
            profundidade = 5
            melhor_coluna, pontuacao = self.minimaxComPoda(tabuleiro, profundidade, -np.inf, np.inf, True)
            melhor_coluna, pontuacao = self.buscaComLimiteTempo(tabuleiro, tempo_inicio)

        tempo_gasto = time.time() - tempo_inicio
        return melhor_coluna, pontuacao, tempo_gasto

    # ============================================================
    # MINIMAX E PODA
    # ============================================================

    def minimaxBasico(self, tabuleiro, profundidade, maximizando):
        """
        Implementação básica do algoritmo Minimax sem otimizações.

        Args:
            tabuleiro (Board): estado atual do tabuleiro
            profundidade (int): limite de recursão
            maximizando (bool): True se é a vez da Maquina, False se é a vez do Jogador

        Returns:
            tuple[int, float]: (melhor_coluna, pontuação estimada)
        """
        self.nos_avaliados += 1

        vencedor = tabuleiro.getVencedor()
        if vencedor != 0 or profundidade == 0 or tabuleiro.isTabuleiroCompleto():
            return -1, self.avaliarPosicao(tabuleiro)

        movimentos_validos = tabuleiro.getMovimentosValidos()

        if maximizando:
            melhor_pontuacao = -np.inf
            melhor_coluna = movimentos_validos[0]

            for coluna in movimentos_validos:
                tabuleiro.addPeca(coluna, 2)
                _, pontuacao = self.minimaxBasico(tabuleiro, profundidade - 1, False)
                tabuleiro.removePeca(coluna)

                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_coluna = coluna

            return melhor_coluna, melhor_pontuacao
        else:
            melhor_pontuacao = np.inf
            melhor_coluna = movimentos_validos[0]

            for coluna in movimentos_validos:
                tabuleiro.addPeca(coluna, 1)
                _, pontuacao = self.minimaxBasico(tabuleiro, profundidade - 1, True)
                tabuleiro.removePeca(coluna)

                if pontuacao < melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_coluna = coluna

            return melhor_coluna, melhor_pontuacao

    def minimaxComPoda(self, tabuleiro, profundidade, alfa, beta, maximizando):
        """
        Implementa o algoritmo Minimax com poda alfa-beta.

        Args:
            tabuleiro (Board): estado atual do jogo
            profundidade (int): limite de profundidade da recursão
            alfa (float): melhor valor mínimo encontrado até agora
            beta (float): melhor valor máximo encontrado até agora
            maximizando (bool): True se é o turno da Maquina

        Returns:
            tuple[int, float]: (melhor_coluna, pontuação estimada)
        """
        self.nos_avaliados += 1

        vencedor = tabuleiro.getVencedor()
        if vencedor != 0 or profundidade == 0 or tabuleiro.isTabuleiroCompleto():
            return -1, self.avaliarPosicao(tabuleiro)

        movimentos_validos = tabuleiro.getMovimentosValidos()

        if self.nivel_dificuldade == 3:
            movimentos_validos = self.ordenarMovimentos(tabuleiro, movimentos_validos)

        if maximizando:
            melhor_pontuacao = -np.inf
            melhor_coluna = movimentos_validos[0]

            for coluna in movimentos_validos:
                tabuleiro.addPeca(coluna, 2)
                _, pontuacao = self.minimaxComPoda(tabuleiro, profundidade - 1, alfa, beta, False)
                tabuleiro.removePeca(coluna)

                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_coluna = coluna

                alfa = max(alfa, pontuacao)
                if beta <= alfa:
                    break

            return melhor_coluna, melhor_pontuacao
        else:
            melhor_pontuacao = np.inf
            melhor_coluna = movimentos_validos[0]

            for coluna in movimentos_validos:
                tabuleiro.addPeca(coluna, 1)
                _, pontuacao = self.minimaxComPoda(tabuleiro, profundidade - 1, alfa, beta, True)
                tabuleiro.removePeca(coluna)

                if pontuacao < melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_coluna = coluna

                beta = min(beta, pontuacao)
                if beta <= alfa:
                    break

            return melhor_coluna, melhor_pontuacao

    def buscaComLimiteTempo(self, tabuleiro, tempo_inicio):
        """
        Executa uma busca iterativa com profundidade crescente até o tempo limite.

        Args:
            tabuleiro (Board): estado atual do tabuleiro
            tempo_inicio (float): timestamp inicial

        Returns:
            tuple[int, float]: (melhor_coluna, pontuação)
        """
        melhor_coluna = tabuleiro.getMovimentosValidos()[0]
        melhor_pontuacao = 0

        for profundidade in range(1, 15):
            if time.time() - tempo_inicio > self.tempo_maximo:
                break

            try:
                coluna, pontuacao = self.minimaxComPoda(tabuleiro, profundidade, -np.inf, np.inf, True)
                melhor_coluna = coluna
                melhor_pontuacao = pontuacao
            except:
                break

        return melhor_coluna, melhor_pontuacao

    # ============================================================
    # HEURÍSTICAS E AVALIAÇÃO
    # ============================================================

    def ordenarMovimentos(self, tabuleiro, movimentos):
        """
        Ordena os movimentos, priorizando as colunas mais próximas do centro.

        Args:
            tabuleiro (Board): estado atual
            movimentos (list[int]): lista de colunas válidas

        Returns:
            list[int]: colunas ordenadas por prioridade estratégica
        """
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

    def avaliarPosicao(self, tabuleiro):
        """
        Chama a função de avaliação adequada conforme o nível de dificuldade.

        Returns:
            float: pontuação heurística da posição
        """
        if self.nivel_dificuldade == 1:
            return self.avaliacaoIniciante(tabuleiro)
        elif self.nivel_dificuldade == 2:
            return self.avaliacaoIntermediaria(tabuleiro)
        else:
            return self.avaliacaoProfissional(tabuleiro)

    # ---- Avaliações específicas ----

    def avaliacaoIniciante(self, tabuleiro):
        """Heurística simples baseada em contagem de pares e trios."""
        vencedor = tabuleiro.getVencedor()
        if vencedor == 2:
            return 1000
        elif vencedor == 1:
            return -1000

        pontuacao = 0
        pontuacao += self.contarJanelas(tabuleiro, 2, 3) * 5
        pontuacao += self.contarJanelas(tabuleiro, 2, 2) * 2
        pontuacao -= self.contarJanelas(tabuleiro, 1, 3) * 5
        pontuacao -= self.contarJanelas(tabuleiro, 1, 2) * 2
        return pontuacao

    def avaliacaoIntermediaria(self, tabuleiro):
        """Heurística intermediária com peso maior para trios e controle central."""
        vencedor = tabuleiro.getVencedor()
        if vencedor == 2:
            return 10000
        elif vencedor == 1:
            return -10000

        pontuacao = 0
        pontuacao += self.contarJanelas(tabuleiro, 2, 3) * 50
        pontuacao += self.contarJanelas(tabuleiro, 2, 2) * 10
        pontuacao += self.contarJanelas(tabuleiro, 2, 1) * 1
        pontuacao -= self.contarJanelas(tabuleiro, 1, 3) * 80
        pontuacao -= self.contarJanelas(tabuleiro, 1, 2) * 15
        pontuacao -= self.contarJanelas(tabuleiro, 1, 1) * 2

        coluna_central = tabuleiro.colunas // 2
        contador_central = sum(1 for linha in range(tabuleiro.linhas)
                               if tabuleiro.grid[linha][coluna_central] == 2)
        pontuacao += contador_central * 6
        return pontuacao

    def avaliacaoProfissional(self, tabuleiro):
        """Heurística avançada considerando padrões e futuro."""
        vencedor = tabuleiro.getVencedor()
        if vencedor == 2:
            return 100000
        elif vencedor == 1:
            return -100000

        pontuacao = 0
        pontuacao += self.avaliarSequenciasAvancadas(tabuleiro, 2) * 100
        pontuacao -= self.avaliarSequenciasAvancadas(tabuleiro, 1) * 120
        pontuacao += self.avaliarForcaPosicao(tabuleiro, 2) * 10
        pontuacao -= self.avaliarForcaPosicao(tabuleiro, 1) * 12
        pontuacao += self.avaliarAmeacas(tabuleiro, 2) * 1000
        pontuacao -= self.avaliarAmeacas(tabuleiro, 1) * 1200
        return pontuacao

    # ============================================================
    # FUNÇÕES AUXILIARES
    # ============================================================

    def contarJanelas(self, tabuleiro, jogador, tamanho):
        """
        Conta quantas "janelas" (grupos de 4) têm a quantidade alvo de peças do jogador.

        Args:
            tabuleiro (Board): estado atual
            jogador (int): 1 (Jogador) ou 2 (Maquina)
            tamanho (int): tamanho da sequência (2, 3 ou 4)

        Returns:
            int: número de janelas que atendem ao critério
        """
        contador = 0
        grid = tabuleiro.grid

        for linha in range(tabuleiro.linhas):
            for coluna in range(tabuleiro.colunas - 3):
                janela = grid[linha, coluna:coluna+4]
                if self.avaliarJanela(janela, jogador, tamanho):
                    contador += 1

        for linha in range(tabuleiro.linhas - 3):
            for coluna in range(tabuleiro.colunas):
                janela = grid[linha:linha+4, coluna]
                if self.avaliarJanela(janela, jogador, tamanho):
                    contador += 1

        for linha in range(tabuleiro.linhas - 3):
            for coluna in range(tabuleiro.colunas - 3):
                janela = [grid[linha+i, coluna+i] for i in range(4)]
                if self.avaliarJanela(janela, jogador, tamanho):
                    contador += 1

                janela = [grid[linha+3-i, coluna+i] for i in range(4)]
                if self.avaliarJanela(janela, jogador, tamanho):
                    contador += 1

        return contador

    def avaliarJanela(self, janela, jogador, tamanho_alvo):
        """Verifica se uma janela contém exatamente a quantidade alvo de peças do jogador."""
        janela = np.array(janela)
        contador_jogador = np.sum(janela == jogador)
        contador_vazio = np.sum(janela == 0)
        oponente = 1 if jogador == 2 else 2
        contador_oponente = np.sum(janela == oponente)

        return (contador_jogador == tamanho_alvo and
                contador_vazio == 4 - tamanho_alvo and
                contador_oponente == 0)

    def avaliarSequenciasAvancadas(self, tabuleiro, jogador):
        """Avalia sequências parciais (2 e 3 em linha) com pesos proporcionais."""
        return (self.contarJanelas(tabuleiro, jogador, 3) * 5 +
                self.contarJanelas(tabuleiro, jogador, 2) * 2)

    def avaliarForcaPosicao(self, tabuleiro, jogador):
        """Dá pontuação adicional para peças próximas ao centro do tabuleiro."""
        pontuacao = 0
        coluna_central = tabuleiro.colunas // 2

        for linha in range(tabuleiro.linhas):
            if tabuleiro.grid[linha][coluna_central] == jogador:
                pontuacao += 3
        return pontuacao

    def avaliarAmeacas(self, tabuleiro, jogador):
        """Calcula possíveis trincas que podem se tornar vitória no próximo turno."""
        return self.contarJanelas(tabuleiro, jogador, 3) * 10
