#!/usr/bin/env python
# Connect Four Game - TDE2 Implementation
# Autor: Alexandre Marques Tortoza Canoa

from colors import bcolors
from board import Board
from agent import AgenteIA
from utils import showTabuleiro, getJogada, escolherDificuldade


def main():
    """
    Função principal que executa o jogo Connect Four.

    Fluxo geral:
        1. Exibe o título e as instruções iniciais.
        2. Solicita a dificuldade escolhida pelo jogador.
        3. Cria a instância da Maquina e do tabuleiro.
        4. Alterna os turnos entre o jogador e a Maquina até o jogo terminar.
        5. Mostra o resultado final (vitória, derrota ou empate).

    Regras:
        - O Jogador sempre joga primeiro.
        - As peças do Jogador são vermelhas.
        - As peças da Maquina são amarelas.

    O jogo termina quando:
        - Um jogador conecta quatro peças seguidas (horizontal, vertical ou diagonal).
        - O tabuleiro é preenchido completamente (empate).
    
    """
    print(f"{bcolors.BOLD}{bcolors.BLUE}=== CONNECT FOUR - TDE2 ==={bcolors.ENDC}")
    print("Humano vs Maquina")
    print("Pode Começar!\n")

    dificuldade = escolherDificuldade()
    agente_ia = AgenteIA(dificuldade)
    tabuleiro = Board()
    jogador_vencedor = 0
    turno_humano = True

    print(f"\n{bcolors.GREEN}[_start_]!{bcolors.ENDC}")
    showTabuleiro(tabuleiro.getTabuleiro())

    while jogador_vencedor == 0 and not tabuleiro.isTabuleiroCompleto():
        if turno_humano:
            print(f"{bcolors.RED}Vez do jogador:{bcolors.ENDC}")
            coluna_humano = getJogada()
            if tabuleiro.isMovimentoValido(coluna_humano):
                tabuleiro.addPeca(coluna_humano, 1)
                turno_humano = False
            else:
                print("Movimento inválido! Coluna cheia.")
                continue
        else:
            print(f"{bcolors.YELLOW}Vez da Maquina:{bcolors.ENDC}")
            print("Clocks going tick...")
            melhor_coluna, pontuacao_avaliacao, tempo_gasto = agente_ia.getMelhorJogada(tabuleiro)
            tabuleiro.addPeca(melhor_coluna, 2)
            colunas_letras = ['a', 's', 'd', 'f', 'g', 'h', 'j']
            print(f"A Maquina jogou na coluna: {bcolors.BOLD}{colunas_letras[melhor_coluna]}{bcolors.ENDC}")
            print(f"gastou: {tempo_gasto:.3f}s")
            print(f"Pontuação: {pontuacao_avaliacao:.2f}")
            print(f"Nós avaliados: {agente_ia.nos_avaliados}")
            turno_humano = True

        showTabuleiro(tabuleiro.getTabuleiro())
        jogador_vencedor = tabuleiro.getVencedor()

    print(f"\n{bcolors.BOLD}=== RESULTADO ==={bcolors.ENDC}")
    if jogador_vencedor == 1:
        print(f"{bcolors.RED}{bcolors.BOLD}Você não perdeu !!!{bcolors.ENDC}")
    elif jogador_vencedor == 2:
        print(f"{bcolors.YELLOW}{bcolors.BOLD}As Máquinas venceram{bcolors.ENDC}")
    else:
        print(f"{bcolors.CYAN}{bcolors.BOLD}Empate 😭 {bcolors.ENDC}")


if __name__ == "__main__":
    main()
