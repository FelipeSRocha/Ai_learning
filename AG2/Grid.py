import colors as cl
import numpy as np
import pygame
import random

occupied_array = np.zeros((2, 3), dtype=bool)
class Grid:
    """test"""
    def __init__(self, width, height, cell_Size):

        self.width = width
        self.height = height

        self.cols = width // cell_Size
        self.rows = height // cell_Size

        self.max_col_number = self.cols-1
        self.max_row_number = self.rows-1
        self.cell_Size = cell_Size

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grid com Pygame")

        self.grid_occupied = np.full((self.rows, self.cols), 0, dtype=int)
        self.grid_function = np.full((self.rows, self.cols), 0, dtype=int)

    def mark_cell(self, row, col, value):
        """Marca uma célula como ocupada."""
        if 0 <= row <= self.max_row_number and 0 <= col <= self.max_col_number:
            self.grid_occupied[row][col] = value
        else:
            print(f"Índices {row, col} fora do limite do array {self.max_row_number, self.max_col_number}")

    def find_random_empty_cell(self):
        """Retorna uma tupla de coordenadas X e Y, retorna -1 caso não tenha celulas vazias"""
        empty_cells = np.where(self.grid_occupied == 0)
        if(len(empty_cells[0])>0):
            index = random.randint(0,len(empty_cells[0])-1)
            return empty_cells[0][index], empty_cells[1][index]
            
        return -1,-1
    
    def verify_move_agent(self, action, row, col, update):
        """Retorna (row, col) da nova posição, se estiver ocupada volta a posição original, se não volta a nova posição"""
        new_row = row
        new_col = col

        if action == 0 :
            new_col += 1
        
        elif action == 1 :
            new_col -= 1

        elif action == 2 :
            new_row += 1
        
        elif action == 3 :
            new_row -= 1
        
        if new_col < 0 or new_col >= self.cols:
            new_col = col
        if new_row < 0 or new_row >= self.rows:
            new_row = row
        
        if self.grid_occupied[new_row][new_col] == 0:
            # print(f"Movido para {new_row, new_col}")
            if(update):
                self.mark_cell(row, col, 0)
                self.mark_cell(new_row, new_col, 1)
            return new_row, new_col
        else:
            # print(f"Celula ocupada, mantendo {row, col}")
            return row, col
        
    def calculate_state(self, agent):
        dist_col = self.cols/2 - agent.col
        dist_row = self.rows/2 - agent.row

        if 0 < agent.row-1 < self.max_row_number:
            up_cell = self.grid_occupied[agent.row-1, agent.col]
        else:
            up_cell = 1

        if 0 < agent.row+1 < self.max_row_number:
            down_cell = self.grid_occupied[agent.row+1, agent.col]
        else:
            down_cell = 1
        
        if 0 < agent.col-1 < self.max_col_number:
            left_cell = self.grid_occupied[agent.row, agent.col-1]
        else:
            left_cell = 1

        if 0 < agent.col+1 < self.max_col_number:
            right_cell = self.grid_occupied[agent.row, agent.col+1]
        else:
            right_cell = 1

        return dist_col, dist_row, up_cell, down_cell, left_cell, right_cell