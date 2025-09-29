#!/usr/bin/env python
# Connect Four Game - TDE2 Implementation
# Alexandre Marques Tortoza Canoa

import numpy as np
import time
from typing import Tuple, List

class bcolors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

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
        return [coluna for coluna in range(self.colunas) if self.isMovimentoValido(coluna)]

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

def showTabuleiro(tabuleiro):
    print("\n" * 2)
    linhas = len(tabuleiro)
    colunas = len(tabuleiro[0])
    print(f"{bcolors.BLUE}==========================={bcolors.ENDC}")
    print(f"{bcolors.CYAN}[a] [s] [d] [f] [g] [h] [j]{bcolors.ENDC}")
    print(f"{bcolors.BLUE}==========================={bcolors.ENDC}\n")

    for i in range(linhas):
        linha_str = ""
        for j in range(colunas):
            if tabuleiro[i][j] == 0:
                linha_str += "[ ] "
            elif tabuleiro[i][j] == 1:
                linha_str += f"[{bcolors.RED}{bcolors.BOLD}⬤{bcolors.ENDC}] "
            elif tabuleiro[i][j] == 2:
                linha_str += f"[{bcolors.YELLOW}{bcolors.BOLD}⬤{bcolors.ENDC}] "
        print(linha_str)

    print(f"{bcolors.BLUE}==========================={bcolors.ENDC}")

def getJogada():
    letras_para_numeros = {'a': 0, 's': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'j': 6}

    while True:
        posicao = input("Qual posição deseja jogar? ").strip().lower()
        if posicao in letras_para_numeros:
            posicao = letras_para_numeros[posicao]
        else:
            try:
                posicao = int(posicao) - 1
            except ValueError:
                print("Entrada inválida, tente novamente.")
                continue
        if 0 <= posicao <= 6:
            return posicao
        else:
            print("Posição inválida, tente de novo...")

def escolherDificuldade():
    print(f"{bcolors.GREEN}Escolha o nível de dificuldade:{bcolors.ENDC}")
    print("1 - Iniciante (Minimax básico, profundidade 3)")
    print("2 - Intermediário (Minimax com poda alfa-beta, profundidade 5)")  
    print("3 - Profissional (Minimax avançado, profundidade adaptativa, 3s limite)")

    while True:
        try:
            escolha = int(input("Digite sua escolha (1, 2 ou 3): "))
            if escolha in [1, 2, 3]:
                return escolha
            else:
                print("Escolha inválida. Digite 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def main():
    print(f"{bcolors.BOLD}{bcolors.BLUE}=== CONNECT FOUR - TDE2 ==={bcolors.ENDC}")
    print("Humano (Vermelho) vs IA (Amarelo)")
    print("O humano sempre joga primeiro!\n")

    dificuldade = escolherDificuldade()
    agente_ia = AgenteIA(dificuldade)

    tabuleiro = Board()
    jogador_vencedor = 0
    turno_humano = True

    print(f"\n{bcolors.GREEN}Iniciando jogo!{bcolors.ENDC}")
    showTabuleiro(tabuleiro.getTabuleiro())

    while jogador_vencedor == 0 and not tabuleiro.isTabuleiroCompleto():
        if turno_humano:
            print(f"{bcolors.RED}Vez do jogador humano (vermelho):{bcolors.ENDC}")
            coluna_humano = getJogada()

            if tabuleiro.isMovimentoValido(coluna_humano):
                tabuleiro.addPeca(coluna_humano, 1)
                turno_humano = False
            else:
                print("Movimento inválido! Coluna cheia. Tente outra coluna.")
                continue
        else:
            print(f"{bcolors.YELLOW}Vez da IA (amarelo):{bcolors.ENDC}")
            print("IA pensando...")

            melhor_coluna, pontuacao_avaliacao, tempo_gasto = agente_ia.getMelhorMovimento(tabuleiro)
            tabuleiro.addPeca(melhor_coluna, 2)

            colunas_letras = ['a', 's', 'd', 'f', 'g', 'h', 'j']
            print(f"IA jogou na coluna: {bcolors.BOLD}{colunas_letras[melhor_coluna]}{bcolors.ENDC}")
            print(f"Tempo gasto: {tempo_gasto:.3f}s")
            print(f"Pontuação de avaliação: {pontuacao_avaliacao:.2f}")
            print(f"Nós avaliados: {agente_ia.nos_avaliados}")

            turno_humano = True

        showTabuleiro(tabuleiro.getTabuleiro())

        jogador_vencedor = tabuleiro.getVencedor()

    print(f"\n{bcolors.BOLD}=== RESULTADO FINAL ==={bcolors.ENDC}")
    if jogador_vencedor == 1:
        print(f"{bcolors.RED}{bcolors.BOLD}🎉 HUMANO VENCEU! 🎉{bcolors.ENDC}")
    elif jogador_vencedor == 2:
        print(f"{bcolors.YELLOW}{bcolors.BOLD}🤖 IA VENCEU! 🤖{bcolors.ENDC}")
    else:
        print(f"{bcolors.CYAN}{bcolors.BOLD}⚖️  EMPATE! ⚖️{bcolors.ENDC}")

if __name__ == "__main__":
    main()
