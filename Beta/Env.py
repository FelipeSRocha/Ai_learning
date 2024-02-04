import pygame

clock = pygame.time.Clock()

class Ambiente:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.scenarios = []
        self.foods = []
        self.agentes = []

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

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

            if len(keys):
                for agente in self.agentes:
                    agente.move(keys, self.scenarios)
                
            for food in self.foods:
                food.verifyColision(agente,self.scenarios)

            self.draw_ambient()

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()


        pass
