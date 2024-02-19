import pygame
import random
import colors as cl
from screen import screen, segment_hor, segment_ver, segment_size

class Wall:
    def __init__(self, screen, position, size):
        self.type = 'wall'
        self.position = position
        self.size = size
        self.screen = screen
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
    
    def draw(self):
        # Implementação básica, subclasses podem sobrescrever
        pygame.draw.rect(self.screen, cl.RED, self.rect)
    
    def interact(self, agent):
        # Método genérico para interação; sobrescreva em subclasses
        pass

class Food:
    def __init__(self, position, screen, radius):
        self.type = 'food'
        self.x = position[0]
        self.y = position[1]
        self.radius = radius
        self.screen = screen
        self.color = cl.BLUE
        self.rect = pygame.Rect(position[0], position[1], 0, 0)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def random_spawn(self):

        pass

    def Eated(self):
        print("Comida consumida!")
        # Mova a comida para uma nova posição
        # self.position = (nova_posicao_x, nova_posicao_y)
        # self.rect.x = nova_posicao_x
        # self.rect.y = nova_posicao_y

    def verifyIfInside(self, x, y ):
        dx = self.x - x
        dy = self.y - y
        distancia = (dx**2 + dy**2) ** 0.5
        return distancia < self.radius

    def verifyColision(self, agente, scenarios, ambient):
        dx = self.x - agente.x
        dy = self.y - agente.y
        distancia = (dx**2 + dy**2) ** 0.5
        if distancia < (self.radius + agente.radius):
            self.find_food_place(scenarios)
            ambient.eated_food += 1
    
    def find_food_place(self,scenarios):
        free_segments = []
        for x in range(segment_hor):
            for y in range(segment_ver):
                segmento = pygame.Rect(x * segment_size, y * segment_size, segment_size, segment_size)
                if not any(obj.rect.colliderect(segmento) for obj in scenarios):
                    free_segments.append(segmento)
        if free_segments:
            segmento_escolhido = random.choice(free_segments)
            self.x, self.y = (segmento_escolhido.x + (segment_size ) // 2, 
                            segmento_escolhido.y + (segment_size) // 2)
        
        return False