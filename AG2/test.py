import pygame
import colors as cl
import math
import numpy as np

class Grid:
    def __init__(self, width, height, cell_Size, agent):
        self.width = width
        self.height = height
        self.cell_Size = cell_Size
        self.GRID_WIDTH = self.width // self.cell_Size
        self.GRID_HEIGHT = self.height  // self.cell_Size
        self.agent = agent
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grid com Pygame")

        self.grid = self.create_grid()
        self.draw_grid()
        self.run()
    
    def create_grid(self):
        grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        print("criando grid")
        for y in range(self.height):
            for x in range(self.width):
                value = 3*x + 5*y
                sqrt = math.sqrt(value)
 
                grid[y][x] = {
                        'ocup': False,
                        'function': '',
                        }
                if int(sqrt) ** 2 == value:
                    grid[y][x] = {
                        'ocup': False,
                        'function': 'food',
                        } 
                value = 25*x + 18*y
                sqrt = math.sqrt(value)
                if int(sqrt) ** 2 == value:
                    grid[y][x] = {
                        'ocup': False,
                        'function': 'reproduce',
                        } 

        return grid
    
    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if(self.grid[y][x]['function'] == 'food'):
                    cell_color = cl.GREEN
                    pygame.draw.rect(self.screen, cell_color, (x * self.cell_Size, y * self.cell_Size, self.cell_Size, self.cell_Size))
                elif(self.grid[y][x]['function'] == 'reproduce'):
                    cell_color = cl.PINK
                    pygame.draw.rect(self.screen, cell_color, (x * self.cell_Size, y * self.cell_Size, self.cell_Size, self.cell_Size))

        
        # for x in range(0, self.width, self.cell_Size):
        #     pygame.draw.line(self.screen, cl.GRAY, (x, 0), (x, self.width))
        # for y in range(0, self.height, self.cell_Size):
        #     pygame.draw.line(self.screen, cl.GRAY, (0, y), (self.width, y))

    
    def move_agent(self, key):
        new_x = self.agent.x 
        new_y = self.agent.y
        if key == pygame.K_LEFT:
            new_x = self.agent.x - 1
        if key == pygame.K_RIGHT:
            new_x = self.agent.x + 1
        if key == pygame.K_UP:
            new_y = self.agent.y - 1
        if key == pygame.K_DOWN:
            new_y = self.agent.y + 1

        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            # if self.grid[new_y][new_x] is None:  # Checa se o espaço está livre
                # Atualiza as posições do agente
                # self.grid[agent.y][agent.x] = None
                # self.grid[new_y][new_x] = agent
            self.agent.x, self.agent.y = new_x, new_y
                # return True
        # return False
    
    def draw_agent(self):
        # pygame.draw.rect(self.screen, cl.BLUE, (1 * self.cell_Size, 1 * self.cell_Size, self.cell_Size, self.cell_Size))
        pygame.draw.circle(self.screen, cl.BLUE, (self.agent.x * self.cell_Size + self.cell_Size/2, self.agent.y * self.cell_Size +  self.cell_Size/2), self.cell_Size/2)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                
                if event.type == pygame.KEYDOWN and not event.key == pygame.K_ESCAPE:
                    self.move_agent(event.key)

                    self.screen.fill(cl.BLACK)
                    self.draw_grid()
                    # Adicione aqui a lógica para desenhar agentes e itens
                    # Por exemplo, para um agente na posição (1, 1):
                    self.draw_agent()
                    
                    pygame.display.flip()

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

agent = Agent(1, 1)
env = Grid(1200,800,20, agent)