import tensorflow as tf
from keras import layers
import numpy as np
import random
from collections import deque


state_size = 2   # Define the size of your state
action_size = 4  # Assuming 4 possible actions: up, down, left, right

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=4000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.loss_history = []
        self.moves_history = []
        self.episodes_history = []

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = tf.keras.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = np.array([state])  # Reshape para 2D (adicionando batch dimension)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size, moves, episode):
        if len(agent.memory) >= agent.memory.maxlen:
            return
        minibatch = random.sample(self.memory, batch_size)

        states = np.array([sample[0] for sample in minibatch]).reshape(batch_size, -1)
        next_states = np.array([sample[3] for sample in minibatch]).reshape(batch_size, -1)

        # Predict Q-values for starting and next states
        Q_values = self.model.predict(states)
        next_Q_values = self.model.predict(next_states)

        # Setup training data
        X_train, y_train = [], []
        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            target = reward
            if not done:
                target += self.gamma * np.amax(next_Q_values[i])
            # Update the target for the action taken
            target_f = Q_values[i]
            target_f[action] = target

            # Add to training data
            X_train.append(state)
            y_train.append(target_f)

        # Fit the model with the entire batch
        history = self.model.fit(np.array(X_train), np.array(y_train), epochs=1, verbose=0)
        loss = history.history['loss'][0]
        self.loss_history.append(loss)
        self.moves_history.append(moves)
        self.episodes_history.append(episode)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    
    def save(self, filename):
        self.model.save(filename)

# Assuming you have defined state_size and action_size
agent = DQNAgent(state_size, action_size)
