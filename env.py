import pygame
import random
import math
import os

# Define cores, tamanho da tela, etc.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)  # Color for the food
GREENER = (0, 255, 0)  # Color for the food in range
BLUE = (0, 0, 255)  # Color for the vision range
#... outros códigos de configuração ...

class ambient:
    def __init__(self, test_mode):
        pygame.init()
        self.test_mode = test_mode
        self.total_movements = 500
        self.steps = 0
        self.total_food = 5
        self.eated_food = 0
        self.points = 100
        self.speed = 20
        self.quit = False
        self.done = False
        self.width, self.height = 200, 200
        self.food = self.spawn_food()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Cell Simulation")

        self.cell = pygame.Rect(400, 300, 20, 20) 
        self.cell_speed = 20
        self.cell_vision_radius=200

        self.last_action = 0
        self.action = 0
        self.last_state = self.calculate_state()
        self.state = self.calculate_state()

        if(self.test_mode):
            self.clock.tick(60)
            self.draw_env()

    def draw_env(self):
        if(self.test_mode):
             # Fill the background
            self.screen.fill(BLACK)

            # Draw the cell and the vision range
            self.draw_cell()

            # Check if food is visible and draw it
            # if is_food_visible(cell, food, cell_vision_radius):
            self.draw_food()
            
            # Update the display
            pygame.display.flip()

              # Limit the game to 60 frames per second

    # Food representation
    def spawn_food(self):
        return pygame.Rect(random.randint(0, self.width-20), random.randint(0, self.height-20), 20, 20)

    def draw_cell(self):
        pygame.draw.rect(self.screen, WHITE, self.cell)
    
    def draw_food(self):
        pygame.draw.rect(self.screen, GREEN, self.food)

    def isDone(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True

    def verifyState (self):
        if(self.steps>=self.total_movements or self.eated_food>=self.total_food):
            self.done = True

    def step(self, action):
        # Implemente a lógica para mover a célula e retornar o novo estado, recompensa, e done
        if action == 0:  # Up
            self.cell.y += self.speed
        elif action == 1:  # Down
            self.cell.y -= self.speed
        elif action == 2:  # Left
            self.cell.x -= self.speed
        elif action == 3:  # Right
            self.cell.x += self.speed

        # Ensure the self.cell stays within the window bounds
        self.cell.x = max(0, min(self.cell.x, self.width - self.width))
        self.cell.y = max(0, min(self.cell.y, self.height - self.height))

        self.steps =+ 1
        self.points =-1

        new_state = self.calculate_state()

        self.updateActionState(action, new_state)

        if self.cell.colliderect(self.food):
            self.eated_food += 1
            self.food = self.spawn_food()  # Respawn food at a new location
            bonus = 50
        else:
            bonus = 0

        self.draw_env()
        return self.calculate_reward(bonus)
    
    def calculate_state(self):
        cell_center = (self.cell.x + self.cell.width / 2, self.cell.y + self.cell.height / 2)
        food_center = (self.food.x + self.food.width / 2, self.food.y + self.food.height / 2)
        dx, dy = food_center[0] - cell_center[0], food_center[1] - cell_center[1]
        distance = math.sqrt(dx**2 + dy**2)

        normalized_dx = dx / self.width
        normalized_dy = dy / self.height
        normalized_distance = distance / (self.width**2 + self.height**2)
        # Include additional features such as last action
        state = [normalized_dx, normalized_dy, normalized_distance, self.last_action]
        return state
    
    def updateActionState(self, action, state):
        self.last_action = self.action
        self.action = action

        self.last_state = self.state
        self.state = state

    def calculate_reward(self, bonus=0):
        reward = bonus
        # Reward or penalize based on distance change
        if self.state[2] < self.last_state[2]:
            reward += 1  # Moving closer to food
        else:
            reward += -1  # Moving away from food

        return reward
    
    def reset(self):
        self.steps = 0
        self.total_food = 5
        self.eated_food = 0
        self.points = 100
        self.done = False
        self.spawn_food()

    def quit(self):
        self.quit = True
        pygame.quit()

# classe da celula

class cell:
    def __init__(self, ambient):
        self.ambient = ambient
        self.speed = 20
        self.vision_radius=200
        self.rep = pygame.Rect(400, 300, 20, 20)  


