import gymnasium as gym
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random

# Criar o ambiente
env = gym.make('CartPole-v1', render_mode='human')
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# Parâmetros
learning_rate = 0.001
gamma = 0.95  # Fator de desconto
epsilon = 1.0  # Exploração inicial
min_epsilon = 0.01
epsilon_decay = 0.995

# Construir a rede neural
model = Sequential()
model.add(Dense(24, input_dim=state_size, activation='relu'))
model.add(Dense(24, activation='relu'))
model.add(Dense(action_size, activation='linear'))
model.compile(loss='mse', optimizer=Adam(learning_rate=learning_rate))

# Treinamento
episodes = 10
for e in range(episodes):
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    for time in range(500):
        env.render()
        if np.random.rand() <= epsilon:
            action = random.randrange(action_size)
        else:
            action = np.argmax(model.predict(state)[0])

        next_state, reward, done, _, _ = env.step(action)
        reward = reward if not done else -10
        next_state = np.reshape(next_state, [1, state_size])
        
        # Ajustar o modelo
        target = reward + gamma * np.amax(model.predict(next_state)[0])
        target_f = model.predict(state)
        target_f[0][action] = target
        model.fit(state, target_f, verbose=0)

        state = next_state
        if done:
            print(f"Episódio: {e + 1}/{episodes}, Pontuação: {time}")
            break

    if epsilon > min_epsilon:
        epsilon *= epsilon_decay

env.close()