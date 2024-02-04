import pygame
import sys
import random
import math
import os
import numpy as np

from dqn_agent import DQNAgent
from keras.models import load_model

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# state_size = 6  # Define the size of your state
# action_size = 4  # Assuming 4 possible actions: up, down, left, right
# model_path = "path_to_save_model.h5"
# agent = DQNAgent(state_size, action_size)

# if os.path.exists(model_path):
#     agent.model = load_model(model_path)
#     print('Using a pre-existing Model')
# else:
#     agent.model = agent._build_model() 
#     print('Building a new Model')


batch_size = 32  # Training batch size
num_episodes = 100

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cell Simulation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)  # Color for the food
GREENER = (0, 255, 0)  # Color for the food in range
BLUE = (0, 0, 255)  # Color for the vision range

# Cell representation
cell = pygame.Rect(400, 300, 20, 20) # A simple square cell
cell_vision_radius = 200  # Vision range of the cell

# Cell speed
cell_speed = 5
cell_move_dist = 20


# Draw the cell
def draw_cell(screen, cell):
    pygame.draw.rect(screen, WHITE, cell)
# Draw the food
def draw_food(screen, food):
    pygame.draw.rect(screen, GREEN, food)

# Food representation
def spawn_food():
    return pygame.Rect(random.randint(0, width-20), random.randint(0, height-20), 20, 20)

# Check if food is within vision range
def is_food_visible(cell, food, vision_radius):
    cell_center = (cell.x + cell.width / 2, cell.y + cell.height / 2)
    food_center = (food.x + food.width / 2, food.y + food.height / 2)
    distance = math.hypot(food_center[0] - cell_center[0], food_center[1] - cell_center[1])
    return distance <= vision_radius

# Draw the cell and its vision
def draw_cell_and_vision(screen, cell, vision_radius):
    pygame.draw.rect(screen, WHITE, cell)
    pygame.draw.circle(screen, BLUE, (cell.x + 10, cell.y + 10), vision_radius, 1)  # Vision circle

def calculate_distance_angle(cell, food, vision_range):
    cell_center = (cell.x + cell.width / 2, cell.y + cell.height / 2)
    food_center = (food.x + food.width / 2, food.y + food.height / 2)
    dx, dy = food_center[0] - cell_center[0], food_center[1] - cell_center[1]
    distance = math.sqrt(dx**2 + dy**2)

    # if distance <= vision_range:
    angle = math.atan2(dy, dx)
    return distance, angle
    # else:
        # Return special values to indicate food is not visible
        # return None, None

def calculate_state(cell, food, cell_vision_radius):
    food_position = calculate_distance_angle(cell, food, cell_vision_radius)
    if food_position == (None, None):
        food_position = np.array([-1, -1])  # Example for food not visible
    else:
        # Normalize and prepare state for NN
        food_position = np.array(food_position) / np.array([cell_vision_radius, math.pi])
    food_position = food_position.reshape(1, -1)  # Reshape for NN
    normalized_top, normalized_bottom, normalized_left, normalized_right = calculate_boundary_distances(cell, width, height)
    return food_position, normalized_top, normalized_bottom, normalized_left, normalized_right

def calculate_boundary_distances(cell, screen_width, screen_height):
    distance_top = cell.y
    distance_bottom = screen_height - (cell.y + cell.height)
    distance_left = cell.x
    distance_right = screen_width - (cell.x + cell.width)

    # Normalize distances
    normalized_top = distance_top / screen_height
    normalized_bottom = distance_bottom / screen_height
    normalized_left = distance_left / screen_width
    normalized_right = distance_right / screen_width

    return normalized_top, normalized_bottom, normalized_left, normalized_right

def move_cell(cell, action):
    """
    Moves the cell based on the given action.

    Parameters:
        cell (pygame.Rect): The cell to move.
        action (int): The action to take (0: up, 1: down, 2: left, 3: right).
        move_dist (int): Distance to move the cell.
        screen_width (int): Width of the screen.
        screen_height (int): Height of the screen.
    """
    if action == 0:  # Up
        cell.y += cell_move_dist
    elif action == 1:  # Down
        cell.y -= cell_move_dist
    elif action == 2:  # Left
        cell.x -= cell_move_dist
    elif action == 3:  # Right
        cell.x += cell_move_dist

    # Ensure the cell stays within the window bounds
    cell.x = max(0, min(cell.x, width - cell.width))
    cell.y = max(0, min(cell.y, height - cell.height))

# Game loop
food = spawn_food()
running = True
done = False
reward = 1000
moves = 0
number_of_foods = 3
foods_eated = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cell.x -= cell_move_dist
            if event.key == pygame.K_RIGHT:
                cell.x += cell_move_dist
            if event.key == pygame.K_UP:
                cell.y -= cell_move_dist
            if event.key == pygame.K_DOWN:
                cell.y += cell_move_dist
            if event.key == pygame.K_ESCAPE:
                running = False

            cell.x = max(0, min(cell.x, width - cell.width))
            cell.y = max(0, min(cell.y, height - cell.height))
            moves +=1
            # Check for collision
            if cell.colliderect(food):
                foods_eated += 1
                print(f"Foods eated: {foods_eated}/{number_of_foods}")
                food = spawn_food()  # Respawn food at a new location
                reward += 100
                # done = True
            else:
                reward -= 1

            new_state = calculate_state(cell, food, cell_vision_radius)
            # agent.memorize(state, action, reward, new_state, done)

            if moves > 1000 or foods_eated>=number_of_foods:
                running = False

        # Fill the background
        screen.fill(BLACK)

        # Draw the cell and the vision range
        draw_cell_and_vision(screen, cell, cell_vision_radius)

        # Check if food is visible and draw it
        # if is_food_visible(cell, food, cell_vision_radius):
        draw_food(screen, food)
        
        # Update the display
        pygame.display.flip()

    # clock.tick(1000)  # Limit the game to 60 frames per second
print(f"Reward: {reward}, Moves: {moves}, Foods eated: {foods_eated}")

# Save the trained model
# agent.save("path_to_save_model.h5")
# print("Saving Model into: path_to_save_model.h5")
# Exit Pygame
pygame.quit()
sys.exit()