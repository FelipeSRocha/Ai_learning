import random
import numpy as np
import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import load_model
from collections import deque

tf.get_logger().setLevel('ERROR')
class dqn_agent:
    def __init__(self, state_size, action_size, batch_size, testing):
        self.model_path = "path_to_save_model.h5"
        self.testing = testing
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.batch_size = batch_size
        self.epsilon = .1  # Exploration rate
        self.epsilon_decay = 0.990
        self.epsilon_min = 0.01
        self.learning_rate = 0.0015
        self.history = {'steps': [0], 'loss': [], 'episode': []} 

        if os.path.exists(self.model_path):
            print(f"Using pre-existing Model: {self.model_path}")
            self.model = load_model(self.model_path)
        else:
            print(f"Creating new Model")
            self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state, episode):

        if episode >= len(self.history['steps']):
            self.history['steps'].append(0)

        # Incrementa o número de passos para o episódio atual.
        self.history['steps'][episode] += 1

        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state = np.atleast_2d(state)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])  # returns action

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, episode_num):
        minibatch = random.sample(self.memory, self.batch_size)

        # Preparar arrays para states e next_states
        states = np.array([experience[0] for experience in minibatch]).reshape(self.batch_size, -1)
        next_states = np.array([experience[3] for experience in minibatch if not experience[4]]).reshape(-1, self.state_size)

        # Fazer previsões em lote
        targets_f = self.model.predict(states, verbose=0)
        next_state_values = np.amax(self.model.predict(next_states, verbose=0), axis=1)

        # Atualizar os targets para cada experiência no minibatch
        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            target = reward
            if not done:
                target += 0.9 * next_state_values[i]
            targets_f[i][action] = target

        # Treinar o modelo em lote
        history = self.model.fit(states, targets_f, epochs=1, verbose=0)
        self.history['loss'].append(history.history['loss'][0])
        self.history['episode'].append(episode_num)

        # Aplicar o decaimento do epsilon após o treino
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Registrar o histórico de epsilon para análise
        self.history.setdefault('epsilon', []).append(self.epsilon)

    def save_model(self, name):
        self.model.save(name)
