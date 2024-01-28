import env
import os
from dqn_agent import dqn_agent

# Inicialize o ambiente e o agente
env = env.ambient(True)

model_path = "path_to_save_model.h5"
state_size = 4  # Define the size of your state
action_size = 4  # Assuming 4 possible actions: up, down, left, right
num_episodes = 150
batch_size = 32  # Training batch size
agent = dqn_agent(state_size, action_size, batch_size)

# Loop principal do jogo
for episode in range(num_episodes):
    if env.quit:
        break
    env.reset()

    while not env.done:
        action = agent.act(env.state)     

        reward = env.step(action)
        agent.memorize(env.state, action, reward, env.last_state, env.done)


        # Treinamento do agente
        if len(agent.memory) > batch_size:
            agent.replay()

    # Outras operações por episódio...

# Salve o modelo e encerre o pygame
agent.save_model("path_to_save_model.h5")
env.quit()