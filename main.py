#!/usr/bin/env python

import numpy as np
import random

#Gera um tabuleiro aleatorio de matriz
# 0: posicao livre
# 1: posicao ocupada por x
# 2: posicao ocupada po O

def random_board():
  num_moves = random.randint(1,9)
  num_x = (num_moves + 1 ) // 2
  num_o = num_moves // 2

  pieces = [1]*num_x + [2]*num_o + [0]*(9-num_moves)
  np.random.shuffle(pieces)
  return np.array(pieces).reshape(3,3)

#funcao de avaliacao
def evaluation_function(board):
  return possible_wins(board, 1) - possible_wins(board, 2)

def possible_wins(board, player):
  if player == 1:
    opponent = 2
  else:
    opponent = 1

  count = 0

  for i in range(len(board)):
    #linhas
    if opponent not in board[i,:]:
      count+=1
    #colunas
    if opponent not in board[:,i]:
      count+=1

  #diagonal pincipal
  if opponent not in np.diag(board):
    count+=1

  #diagonal secundaria
  if opponent not in np.diag(np.fliplr(board)):
    count+=1

  return count

board =  random_board()
eval = evaluation_function(board)


print(board)
print(eval)


from timeit import default_timer as timer
def compute_eval_by_time(max_time):
  count = 0
  elapsed_time = 0
  start_time = timer ()
  while elapsed_time <= max_time:
    board = random_board()
    eval = evaluation_function(board)
    count+=1
    elapsed_time = timer() - start_time
  return count

max_time = 1
result = compute_eval_by_time(max_time)
print(result)
