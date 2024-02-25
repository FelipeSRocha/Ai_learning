import Grid as gr
import agent as ag
import colors as cl
import os
import neat
# from rtree import index
import pygame

screen_width = 800
screen_height = 800
cell_size = 5
max_steps = screen_width//cell_size
fps = 10000

class Screen:
    def __init__(self, fps):
        # Configura a tela do pygame
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Grid com Pygame")
        self.clock = pygame.time.Clock()
        self.fps = fps

    def reset_draw_screen(self):
        self.screen.fill(pygame.Color('black'))  # Limpa a tela

    def draw_agent(self, agents, grid):

        for agent in agents:
            x = (agent.col)*grid.cell_Size
            y = (agent.row)*grid.cell_Size
                # Calcula o centro do grid
            center_row = grid.rows / 2
            center_col = grid.cols / 2

            # Calcula a distância do agente até o centro do grid
            distance = max(abs(agent.row - center_row), abs(agent.col - center_col))

            # Calcula o máximo valor de distância possível do centro para os cantos do grid
            max_distance = max(center_row, center_col)

            # Calcula o valor para o componente verde baseado na distância (inversamente proporcional)
            value = int((1 - distance / max_distance) * 255)

            # Garante que o valor esteja entre 0 e 255
            value = max(0, min(255, value))

            color = (255, value, 255)
            pygame.draw.rect(self.screen, color, (x, y, grid.cell_Size, grid.cell_Size))


    def tick(self):
        self.clock.tick(self.fps)

class generation:
    def __init__(self):
        self.gen = 0
    def end_generation(self):
        self.gen +=1
def run_simulation(genomes, config):
    print(f'Iniciando Geração {gen.gen}')
    agents = []
    nets = []
    grid = gr.Grid(screen_width, screen_height, cell_size)
    # Inicializa os agentes e as redes neurais para cada genoma
    for genome_id, genome in genomes:
        # if(existing_model):
        #     with open('melhor_genoma.pkl', 'rb') as f:
        #         neural = pickle.load(f)
        #     net = neat.nn.FeedForwardNetwork.create(neural, config)
        # else:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        new_position = grid.find_random_empty_cell()
        agents.append(ag.Agente(*new_position)) 
        grid.mark_cell(*new_position, 1) # Define a posição y baseada no número de agentes
        genome.fitness = 0  # Inicializa o fitness

    print(f"N Agentes {len(genomes)}")
    sc.draw_agent(agents, grid)
    for x in range(max_steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        sc.reset_draw_screen()  # Limpa a tela

        for i, agent in enumerate(agents):
            dist_col, dist_row, up_cell, down_cell, left_cell, right_cell = grid.calculate_state(agent)
            output = nets[i].activate((agent.col, agent.row, agent.last_col, agent.last_row ,dist_col, dist_row, up_cell, down_cell, left_cell, right_cell))  # A entrada da rede é a posição x do bloco
            action = output.index(max(output))  # Escolhe a ação com a maior saída
            agent.move_agent(*grid.verify_move_agent(action, agent.row, agent.col, True))  # Atualiza a posição do bloco

            genomes[i][1].fitness = (grid.rows/2 -abs(agent.row - grid.rows/2)) + (grid.cols/2 - abs(agent.col - grid.cols/2)) # Atualiza o fitness com base na posição x do bloco

        # draw_grid()  # Desenha o grid
        sc.draw_agent(agents, grid)

        pygame.display.flip()  # Atualiza a tela
        sc.tick()
    print('Finalizando Geração')
    gen.end_generation()
    
        
            

sc = Screen(fps)
# Carrega o arquivo de configuração NEAT
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config-feedforward.txt")
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)

p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))
p.add_reporter(neat.StatisticsReporter())
gen = generation()
winner = p.run(run_simulation, 1000)  # Executa a simulação por 50 gerações


