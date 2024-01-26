import pygame
import sys
import random
import math
import os
import numpy as np
import matplotlib.pyplot as plt

from dqn_agent import DQNAgent
from keras.models import load_model

# Initialize Pygame
learning = False

if learning:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


pygame.init()
clock = pygame.time.Clock()

model_path = "path_to_save_model.h5"
state_size = 4  # Define the size of your state
action_size = 4  # Assuming 4 possible actions: up, down, left, right
agent = DQNAgent(state_size, action_size)

if os.path.exists(model_path):
    agent.model = load_model(model_path)
    print('Using a pre-existing Model')
else:
    agent.model = agent._build_model() 
    print('Building a new Model')


batch_size = 32  # Training batch size
num_episodes = 150

# Set up the display
width, height = 200, 200
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

def calculate_distance_angle(cell, food):
    cell_center = (cell.x + cell.width / 2, cell.y + cell.height / 2)
    food_center = (food.x + food.width / 2, food.y + food.height / 2)
    dx, dy = food_center[0] - cell_center[0], food_center[1] - cell_center[1]
    distance = math.sqrt(dx**2 + dy**2)

    return [dx, dy, distance]

def calculate_state(cell, food, last_action):
    dx, dy, distance = calculate_distance_angle(cell, food)
    # Normalize dx, dy, and distance
    normalized_dx = dx / width
    normalized_dy = dy / height
    normalized_distance = distance / (width**2 + height**2)
    # Include additional features such as last action
    state = [normalized_dx, normalized_dy, normalized_distance, last_action]
    return state

def calculate_reward(last_distance, current_distance, reached_goal):
    reward = 0
    # Reward or penalize based on distance change
    if current_distance < last_distance:
        reward = 1  # Moving closer to food
    else:
        reward = -1  # Moving away from food
    
    # Add a substantial reward for reaching the goal
    # if reached_goal:
    #     reward = 50  # Reached the food

    # Penalize for each step to encourage efficiency

    return reward

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


for episode in range(num_episodes):
    # Game loop
    food = spawn_food()
    running = True
    total = 500
    points = total
    moves = 0
    number_of_foods = 5
    foods_eated = 0
    stop = False
    action = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop = True
                    running = False

        state = calculate_state(cell, food, action)
        
        action = agent.act(state)

        move_cell(cell, action)

        new_state = calculate_state(cell, food, action)

        moves +=1
        # Check for collision
        if cell.colliderect(food):
            foods_eated += 1
            food = spawn_food()  # Respawn food at a new location
            goal = True
        else:
            goal = False

        reward_agent = calculate_reward(state[2], new_state[2], goal)

        agent.memorize(state, action, reward_agent, new_state, not running)

        if moves > total or foods_eated>=number_of_foods:
            running = False

        if not learning:

            # Fill the background
            screen.fill(BLACK)

            # Draw the cell and the vision range
            draw_cell_and_vision(screen, cell, cell_vision_radius)

            # Check if food is visible and draw it
            # if is_food_visible(cell, food, cell_vision_radius):
            draw_food(screen, food)
            
            # Update the display
            pygame.display.flip()

            clock.tick(60)  # Limit the game to 60 frames per second
        
    # Train the model with a minibatch from the replay buffer
    if learning:
        agent.replay(batch_size, moves, episode)
    print(f"Episode: {episode}, Moves: {moves}, Foods eated: {foods_eated}")
    print(f" epsilon: {agent.epsilon}")

    if stop:
        break

# Save the trained model
agent.save("path_to_save_model.h5")
print("Saving Model into: path_to_save_model.h5")


fig, ax1 = plt.subplots()

ax1.set_xlabel('Episodes')
ax1.set_ylabel('Loss', color='tab:blue')
ax1.plot(range(num_episodes), agent.loss_history, color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Instantiate a second y-axis sharing the same x-axis
ax2 = ax1.twinx()  
ax2.set_ylabel('Moves', color='tab:red')  
ax2.plot(range(num_episodes), agent.moves_history, color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.show()

# Show the plot
plt.show()
# Exit Pygame
pygame.quit()
sys.exit()