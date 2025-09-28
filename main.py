#!/usr/bin/env python

from src.game.board import Board
from src.game.moves import getJogada
from src.ui.console import showTabuleiro

tabuleiro = Board()
showTabuleiro(tabuleiro.getTabuleiro())

tabuleiro.addPeca(2,1)
tabuleiro.addPeca(2,2)

showTabuleiro(tabuleiro.getTabuleiro())


jogador_vencedor = 0

while jogador_vencedor == 0:
    jogador_vencedor = tabuleiro.getVencedor()

    showTabuleiro(tabuleiro.getTabuleiro())
    j1_coluna =  getJogada()
    tabuleiro.addPeca(j1_coluna,1)

    jogador_vencedor = tabuleiro.getVencedor()

showTabuleiro(tabuleiro.getTabuleiro())
