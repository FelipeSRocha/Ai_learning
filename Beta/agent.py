import math
import pygame
import colors as cl
import screen as sc

import random
import numpy as np
import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import load_model
from collections import deque

testing = True
model_path = "Beta\path_to_save_model.h5"
state_size = 64  # Define the size of your state
action_size = 4  # Assuming 4 possible actions: up, down, left, right
batch_size = 128  # Training batch size

class Agente:
    def __init__(self, position, screen, agent_speed, radius):
        self.x = position[0]
        self.y = position[1]
        self.radius = radius
        self.speed = agent_speed
        self.screen = screen
        self.color = cl.WHITE
        self.num_rays = 32
        self.visionRange = 500
        self.vision_rays = []

        self.lastdistanceToFood = 0
        self.nextdistanceToFood = 0
        self.lastReward = 0
        self.nextReward = 0
        self.lastState = []
        self.nextState = []
        self.dqn_agent = dqn_agent(state_size, action_size, batch_size, testing)

        

    def draw(self, objects, foods):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        self.draw_rays()
        # self.calculateReward()
        
    def draw_rays(self):
        for sc.screen, ray_color , (self.x, self.y), (end_x, end_y) in self.vision_rays:
            pygame.draw.line(sc.screen, ray_color , (self.x, self.y), (end_x, end_y))

    def verifyColision(self, objects):
        for obj in objects:
            if self.colision_calculate(obj):
                return True 
            elif self.x > sc.screen_width or self.x < 0:
                return True
            elif self.y > sc.screen_height or self.y < 0:
                return True
        return False 
        
    def colision_calculate(self,object):
        if object.type == 'wall':
            closest_x = max(object.rect.left, min(self.x, object.rect.right))
            closest_y = max(object.rect.top, min(self.y, object.rect.bottom))
            dx = closest_x - self.x
            dy = closest_y - self.y
            distancia = (dx**2 + dy**2) ** 0.5
            return distancia < self.radius
        return False
    
    def act(self, objects, foods, episode, ambient):    
        if(len(self.lastState) <1):
            self.lastState = self.calculateNewState(objects, foods)   

        action = self.move(objects, episode)
        ambient.steps += 1
        self.nextState = self.calculateNewState(objects, foods)
        self.calculateReward()
        self.dqn_agent.memorize(self.nextState, action, self.nextReward, self.lastState, ambient.done)
        self.resetStates()

        # if keys[pygame.K_LEFT]:
        #     self.x -= self.speed
        # if keys[pygame.K_RIGHT]:
        #     self.x += self.speed
        # if keys[pygame.K_UP]:
        #     self.y -= self.speed
        # if keys[pygame.K_DOWN]:
        #     self.y += self.speed

    def move(self, objects, episode):
        original_x = self.x
        original_y = self.y
        action = self.dqn_agent.act(self.lastState, episode)

        if action == 0:  # Up
            self.y += self.speed
        elif action == 1:  # Down
            self.y -= self.speed
        elif action == 2:  # Left
            self.x -= self.speed
        elif action == 3:  # Right
            self.x += self.speed

        if self.verifyColision(objects):
            self.x=original_x
            self.y=original_y
        return action

    def calculateNewState(self, objects, foods):
        self.vision_rays =[]
        angle_gap = 360 / self.num_rays
        self.nextdistanceToFood = 0
        state = []
        for i in range(self.num_rays):
            angle = math.radians(i * angle_gap)
            end_x, end_y, ray_color, seeFood, distance, objectSaw = self.cast_ray( angle, objects, foods)

            ## Save the distance to food as a self state
            nextdistanceToFood = (self.visionRange-distance)/self.visionRange

            if seeFood and self.nextdistanceToFood < nextdistanceToFood: self.nextdistanceToFood = nextdistanceToFood
            
            state.extend([nextdistanceToFood, objectSaw])
            self.vision_rays.append([sc.screen, ray_color , (self.x, self.y), (end_x, end_y)])
        return state

    def calculateReward(self):
        if self.lastdistanceToFood < self.nextdistanceToFood:
            self.nextReward = 1
        else:
            self.nextReward = 0


    def resetStates(self):
        self.lastdistanceToFood = self.nextdistanceToFood
        self.nextdistanceToFood = 0
        self.lastReward = self.nextReward
        self.nextReward = 0
        self.lastState = self.nextState
        # self.nextState = []
        pass
    def cast_ray(self, angle, objects, foods):
        sin_angle, cos_angle = math.sin(angle), math.cos(angle)
        distance = 0
        hit = False
        ray_color= cl.WHITE
        seeFood = False
        objectSaw = 0
        while not hit and distance < self.visionRange:
            distance += 1
            check_x, check_y = self.x + cos_angle * distance, self.y + sin_angle * distance
            
            for obj in objects:
                if obj.rect.collidepoint((check_x, check_y)):
                    hit = True
                    objectSaw = -1
                    # pygame.draw.circle(sc.screen, cl.RED, (check_x, check_y), 2)
                    break
            
            for obj in foods:
                if obj.verifyIfInside(check_x, check_y):
                    hit = True
                    ray_color= cl.BLUE
                    seeFood = True
                    objectSaw = 1
                    break

        end_x = self.x + math.cos(angle) * distance
        end_y = self.y + math.sin(angle) * distance

        return end_x, end_y, ray_color, seeFood, distance, objectSaw

    def calculateRays(self, objects, foods):
        self.vision_rays =[]
        angle_gap = 360 / self.num_rays
        self.nextdistanceToFood = 0
        self.nextState = []
        for i in range(self.num_rays):
            angle = math.radians(i * angle_gap)
            end_x, end_y, ray_color, seeFood, distance, objectSaw = self.cast_ray( angle, objects, foods)

            ## Save the distance to food as a self state
            nextdistanceToFood = (self.visionRange-distance)/self.visionRange

            if seeFood and self.nextdistanceToFood < nextdistanceToFood: self.nextdistanceToFood = nextdistanceToFood
            
            self.nextState.extend([nextdistanceToFood, objectSaw])
            self.vision_rays.append([sc.screen, ray_color , (self.x, self.y), (end_x, end_y)])


    # def calculate_vision_food(self, foods, x1, y1, x2, y2):
    #     for food in foods:
    #         cx, cy = food.x, food.y
    #         px, py, is_within_segment  = self.ponto_proximo_reta(cx, cy, x1, y1, x2, y2)
        
    #         # Calcula a distância do ponto mais próximo ao centro do círculo
    #         distancia = math.sqrt((px - cx)**2 + (py - cy)**2)
    #         if distancia <= food.radius and is_within_segment:
    #             return True
    #     return False
    
    def ponto_proximo_reta(self, cx, cy, x1, y1, x2, y2):
        reta_vx = x2 - x1
        reta_vy = y2 - y1
        ponto_vx = cx - x1
        ponto_vy = cy - y1
        norma_reta = (reta_vx**2 + reta_vy**2)
        t = max(0, min(1, (ponto_vx * reta_vx + ponto_vy * reta_vy) / norma_reta))
        proximo_x = x1 + t * reta_vx
        proximo_y = y1 + t * reta_vy
        return proximo_x, proximo_y, t >= 0 and t <= 1

class dqn_agent:
    def __init__(self, state_size, action_size, batch_size, testing):
        self.model_path = "Beta/path_to_save_model.h5"
        self.testing = testing
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.batch_size = batch_size
        self.epsilon = 1  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.0010
        self.learning_rate_decay = 0.995  # Exemplo de fator de decaimento
        self.learning_rate_min = 0.0001   # Taxa de aprendizado mínima
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

    def act(self, state, episode ):

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

        self.learning_rate = max(self.learning_rate_min, self.learning_rate * self.learning_rate_decay)
        # Registrar o histórico de epsilon para análise
        self.history.setdefault('epsilon', []).append(self.epsilon)

    def save_model(self, name):
        self.model.save(name)