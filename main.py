#!/usr/bin/env python
# Connect Four Game - TDE2 Implementation
# Alexandre Marques Tortoza Canoa

from colors import bcolors
from board import Board
from agent import AgenteIA
from utils import showTabuleiro, getJogada, escolherDificuldade



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
            print(f"Pontuação: {pontuacao_avaliacao:.2f}")
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
