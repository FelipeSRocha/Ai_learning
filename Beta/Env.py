import pygame
import matplotlib.pyplot as plt

clock = pygame.time.Clock()

class Ambiente:
    def __init__(self, screen, training, num_episodes):
        pygame.init()
        self.screen = screen
        self.scenarios = []
        self.foods = []
        self.agentes = []
        self.done = False
        self.quit = False
        self.training = training
        self.num_episodes = num_episodes
        self.FPS = 10
        self.total_movements = 1000
        self.steps = 0
        self.total_food = 3
        self.eated_food = 0
        self.points = 100
        self.speed = 20

    def add_scenery_item(self, item):
        self.scenarios.append(item)
    
    def add_food_item(self, item):
        self.foods.append(item)

    def add_agente(self, agente):
        self.agentes.append(agente)

    def draw_ambient(self):
        self.screen.fill((0,0,0))  # Limpa a tela
        for agente in self.agentes:
            agente.draw(self.scenarios, self.foods)

        for scenary in self.scenarios:
            scenary.draw()
        
        for food in self.foods:
            food.draw()

    def reset(self):
        self.steps = 0
        self.total_food = 3
        self.eated_food = 0
        # self.points = 100
        self.done = False
        # for food in self.foods:
        #     food.find_food_place(self.scenarios)
    
    def end(self):
        self.quit = True
        pygame.quit()

    def verifyState (self):
        # print(self.steps, self.eated_food, self.total_food)
        if(self.eated_food>=self.total_food or self.steps > self.total_movements):
            self.done = True

    def run(self):
        for episode in range(self.num_episodes):
            if self.quit:
                break
            self.reset()
            while not self.done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.quit()

                # if len(keys):
                for agente in self.agentes:
                    agente.act(episode, self)
                    
                # for food in self.foods:
                #     if food.verifyAgentColision(agente): 
                #         food.respawnFood(self)

                self.verifyState()

                if not self.training:
                    pygame.display.flip()
                    self.draw_ambient()
                    clock.tick(self.FPS)

            print(f"Episode: {episode}, Steps: {self.steps}, Food eated: {self.eated_food}, Epsilon: f{self.agentes[0].dqn_agent.epsilon}")

            for agent in self.agentes:
                if len(agent.dqn_agent.memory) > agent.dqn_agent.batch_size and self.training:
                    agent.dqn_agent.replay(episode)

        self.agentes[0].dqn_agent.save_model(f"Beta/path_to_save_model.h5")

        self.end()
        if(self.training):
            fig, ax1 = plt.subplots()

            ax1.set_xlabel('Episodes')
            ax1.set_ylabel('Loss', color='tab:blue')
            ax1.plot(range(self.num_episodes), self.agentes[0].dqn_agent.history['loss'], color='tab:blue')
            ax1.tick_params(axis='y', labelcolor='tab:blue')

            # Instantiate a second y-axis sharing the same x-axis
            ax2 = ax1.twinx()  
            ax2.set_ylabel('Moves', color='tab:red')  
            ax2.plot(range(self.num_episodes), self.agentes[0].dqn_agent.history['steps'], color='tab:red')
            ax2.tick_params(axis='y', labelcolor='tab:red')

            plt.show()

