import env
import os
from dqn_agent import dqn_agent
import pygame
import matplotlib.pyplot as plt

# Inicialize o ambiente e o agente
testing = True
env = env.ambient(testing)

model_path = "Alpha\path_to_save_model.h5"
state_size = 4  # Define the size of your state
action_size = 4  # Assuming 4 possible actions: up, down, left, right
num_episodes = 100
batch_size = 64  # Training batch size
agent = dqn_agent(state_size, action_size, batch_size, testing)

# Loop principal do jogo
for episode in range(num_episodes):
    if env.quit:
        break
    env.reset()
    while not env.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    env.quit()

        action = agent.act(env.state, episode)     

        reward = env.step(action)
        agent.memorize(env.state, action, reward, env.last_state, env.done)
        env.verifyState()

    print(f"Episode: {episode}, Steps: {env.steps}, Points: {env.points}, Food eated: {env.eated_food}, epsilon: {agent.epsilon}")
    # Treinamento do agente
    if len(agent.memory) > batch_size and not testing:
        agent.replay(episode)

agent.save_model("path_to_save_model.h5")
env.end()
fig, ax1 = plt.subplots()

ax1.set_xlabel('Episodes')
ax1.set_ylabel('Loss', color='tab:blue')
ax1.plot(range(num_episodes), agent.history['loss'], color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Instantiate a second y-axis sharing the same x-axis
ax2 = ax1.twinx()  
ax2.set_ylabel('Moves', color='tab:red')  
ax2.plot(range(num_episodes), agent.history['steps'], color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.show()

# Salve o modelo e encerre o pygame
