import os
import neat
import pygame
import pickle
import random

# Assume que as definições iniciais e a classe Block de Pygame estejam aqui
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
path_neural = 'AG_Model/melhor_genoma.pkl'
if not os.path.exists(path_neural):
    existing_model = False
else:
    existing_model = True

class Agente:
    def __init__(self, y):
        self.width = 1
        self.x = random.randint(1, 99)
        self.y = random.randint(1, 99)
        self.radius = 1
        self.alive = True
    
    def move(self, action):
        if not self.alive:
            return

        if action == 0 :
            self.x += 1
        
        if action == 1 :
            self.x -= 1

        if action == 2 :
            self.y += 1
        
        if action == 3 :
            self.y -= 1
            
        if self.x< 1 or self.x >=SCREEN_WIDTH or self.y< 1 or self.y >=SCREEN_HEIGHT:
            self.alive = False
        

def eval_genomes(genomes, config):
    pygame.init()
    agents = []
    nets = []
    max_step = 100
    y_spacing = SCREEN_HEIGHT / len(genomes)  # Calcula o espaçamento vertical dos agentes

    # Inicializa os agentes e as redes neurais para cada genoma
    for genome_id, genome in genomes:
        if(existing_model):
            with open('melhor_genoma.pkl', 'rb') as f:
                neural = pickle.load(f)
            net = neat.nn.FeedForwardNetwork.create(neural, config)
        else:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        agents.append(Agente(y_spacing * len(agents)))  # Define a posição y baseada no número de agentes
        genome.fitness = 0  # Inicializa o fitness

    for x in range(max_step):
        screen.fill((0, 0, 0))  # Limpa a tela
        # print(nets[1])
        for i, agent in enumerate(agents):
            output = nets[i].activate((agent.x,SCREEN_WIDTH - agent.x, agent.y, SCREEN_HEIGHT - agent.y))  # A entrada da rede é a posição x do bloco
            action = output.index(max(output))  # Escolhe a ação com a maior saída
            agent.move(action)  # Atualiza a posição do bloco
            if 30 < agent.x < 70 and 30 < agent.y < 70:
                cl = (0, 255, 0)
            else:
                cl = (255, 255, 255)

            genomes[i][1].fitness = (-abs(agent.y - 50) + 50)+(-abs(agent.x - 50) + 50)  # Atualiza o fitness com base na posição x do bloco

            # Desenha o agente
            pygame.draw.circle(screen, cl, (agent.x, agent.y), agent.radius)

        pygame.display.flip()  # Atualiza a tela
        clock.tick(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

def run(config_file):
    # Carrega o arquivo de configuração NEAT
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(eval_genomes, 200)  # Executa a simulação por 50 gerações
    return winner

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    winner = run(config_path)

    # Após o treinamento ser concluído e o melhor genoma encontrado
    # with open('AG_Model/melhor_genoma.pkl', 'wb') as f:
    #     pickle.dump(winner, f)