#!/usr/bin/env python

from src.game.board import Board
from src.ui.console import showTabuleiro

tabuleiro = Board()
showTabuleiro(tabuleiro.getTabuleiro())

tabuleiro.addPeca(2,1)
tabuleiro.addPeca(2,2)

showTabuleiro(tabuleiro.getTabuleiro())
