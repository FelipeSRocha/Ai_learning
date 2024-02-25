import colors as cl
import math
import numpy as np
from rtree import index
import os
import neat
import pygame
import agent
import Grid

clock = pygame.time.Clock()

class Env:
    def __init__(self, width, height, cell_Size):
        self.width = width
        self.height = height
        self.cell_Size = cell_Size
        self.max_steps = 40
        self.GRID_WIDTH = self.width // self.cell_Size
        self.GRID_HEIGHT = self.height  // self.cell_Size
        self.local_dir = os.path.dirname(__file__)
        self.config_path = os.path.join(self.local_dir, "config-feedforward.txt")

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grid com Pygame")



        # winner = p.run(self.run_simulation, 500)  # Executa a simulação por 50 gerações
        # self.create_agent(1,1)
        # self.create_agent(7,7)
        # self.add_object_to_rtree()

        # self.draw_grid()
        # self.run()
    
    # def create_agent(self, x,y):
    #     agent = Agent(x,y)
    #     x = (agent.x)*self.cell_Size
    #     y = (agent.y)*self.cell_Size
    #     obj_rect = (x * self.cell_Size, y * self.cell_Size, (x + 1) * self.cell_Size, (y + 1) * self.cell_Size)
    #     idx = len(self.agent)
    #     self.rtree_index.insert(idx, obj_rect)
    #     self.agent.append(agent)

    def add_object_to_rtree(self):
        for idx, cell in enumerate(self.grid):
            x = (cell[0])*self.cell_Size
            y = (cell[1])*self.cell_Size
            obj_rect = (x * self.cell_Size, y * self.cell_Size, (x + 1) * self.cell_Size, (y + 1) * self.cell_Size)
            self.rtree_index.insert(idx, obj_rect)

    def draw_grid(self):
        for idx, cell in enumerate(self.grid):
            x = (cell[0])*self.cell_Size
            y = (cell[1])*self.cell_Size
            pygame.draw.rect(self.screen, cl.BLUE, (x, y, self.cell_Size, self.cell_Size))


        # Calcula o retângulo delimitador do objeto
        # obj_rect = (x * self.cell_Size, y * self.cell_Size, (x + 1) * self.cell_Size, (y + 1) * self.cell_Size)
        # self.rtree_index.insert(obj_id, obj_rect)

    def move_agent(self, action, agent):
        if not agent.alive:
            return

        if action == 0 :
            agent.x += 1
        
        if action == 1 :
            agent.x -= 1

        if action == 2 :
            agent.y += 1
        
        if action == 3 :
            agent.y -= 1
            
        if agent.x< 1 or agent.x >= (self.width/self.cell_Size-1 )or agent.y< 1 or agent.y >=(self.height/self.cell_Size-1):
            agent.alive = False

    def draw_agent(self, agents):
        for agent in agents:
            x = (agent.x)*self.cell_Size
            y = (agent.y)*self.cell_Size

            pygame.draw.rect(self.screen, cl.WHITE, (x, y, self.cell_Size, self.cell_Size))


    
    def run_simulation(self, genomes, config):

        agents = []
        nets = []

        # Inicializa os agentes e as redes neurais para cada genoma
        for genome_id, genome in genomes:
            # if(existing_model):
            #     with open('melhor_genoma.pkl', 'rb') as f:
            #         neural = pickle.load(f)
            #     net = neat.nn.FeedForwardNetwork.create(neural, config)
            # else:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            agents.append(Agente(self.width, self.height, self.cell_Size))  # Define a posição y baseada no número de agentes
            genome.fitness = 0  # Inicializa o fitness


        for x in range(self.max_steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
            self.screen.fill((0, 0, 0))  # Limpa a tela

            for i, agent in enumerate(agents):

                
                output = nets[i].activate((agent.x,self.width - agent.x, agent.y, self.height - agent.y))  # A entrada da rede é a posição x do bloco
                action = output.index(max(output))  # Escolhe a ação com a maior saída
                self.move_agent(action, agent)  # Atualiza a posição do bloco

                genomes[i][1].fitness = +agent.y - agent.x  # Atualiza o fitness com base na posição x do bloco
            self.screen.fill(pygame.Color('black'))  # Limpa a tela
            # self.draw_grid()  # Desenha o grid
            self.draw_agent(agents)

            pygame.display.flip()  # Atualiza a tela
            clock.tick(500)




env = Env(800,800,20)

# def eval_genomes(genomes, config):
#     pygame.init()
#     agents = []
#     nets = []
#     max_step = 100
#     # y_spacing = SCREEN_HEIGHT / len(genomes)  # Calcula o espaçamento vertical dos agentes

#     # Inicializa os agentes e as redes neurais para cada genoma
#     for genome_id, genome in genomes:
#         # if(existing_model):
#         #     with open('melhor_genoma.pkl', 'rb') as f:
#         #         neural = pickle.load(f)
#         #     net = neat.nn.FeedForwardNetwork.create(neural, config)
#         # else:
#         net = neat.nn.FeedForwardNetwork.create(genome, config)
#         nets.append(net)
#         agents.append(Agente())  # Define a posição y baseada no número de agentes
#         genome.fitness = 0  # Inicializa o fitness

#     for x in range(max_step):
#         screen.fill((0, 0, 0))  # Limpa a tela
#         # print(nets[1])
#         for i, agent in enumerate(agents):
#             output = nets[i].activate((agent.x,SCREEN_WIDTH - agent.x, agent.y, SCREEN_HEIGHT - agent.y))  # A entrada da rede é a posição x do bloco
#             action = output.index(max(output))  # Escolhe a ação com a maior saída
#             agent.move(action)  # Atualiza a posição do bloco
#             if 30 < agent.x < 70 and 30 < agent.y < 70:
#                 cl = (0, 255, 0)
#             else:
#                 cl = (255, 255, 255)

#             genomes[i][1].fitness = (-abs(agent.y - 50) + 50)+(-abs(agent.x - 50) + 50)  # Atualiza o fitness com base na posição x do bloco

#             # Desenha o agente
#             pygame.draw.circle(screen, cl, (agent.x, agent.y), agent.radius)

#         pygame.display.flip()  # Atualiza a tela
#         clock.tick(1000)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.quit()



# if __name__ == "__main__":
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, "config-feedforward.txt")
#     winner = run(config_path)

#     # Após o treinamento ser concluído e o melhor genoma encontrado
#     # with open('AG_Model/melhor_genoma.pkl', 'wb') as f:
#     #     pickle.dump(winner, f)