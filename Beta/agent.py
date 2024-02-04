import math
import pygame
import colors as cl
import screen as sc
class Agente:
    def __init__(self, position, screen, agent_speed, radius):
        self.x = position[0]
        self.y = position[1]
        self.radius = radius
        self.speed = agent_speed
        self.screen = screen
        self.color = cl.WHITE
        self.n_rays = 0
    def draw(self, objects, foods):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        self.draw_rays(objects, foods)
        print(self.n_rays)
    def update(self, cenário_items):
        # Lógica para "ver" o cenário e tomar ações
        pass

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
    
    def move(self, keys, objects):
        original_x = self.x
        original_y = self.y

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        if self.verifyColision(objects):
            self.x=original_x
            self.y=original_y

    def cast_ray(self, angle, objects):
        sin_angle, cos_angle = math.sin(angle), math.cos(angle)
        distance = 0
        hit = False

        while not hit and distance < 1000:
            distance += 1
            check_x, check_y = self.x + cos_angle * distance, self.y + sin_angle * distance
            
            for obj in objects:
                if obj.rect.collidepoint((check_x, check_y)):
                    hit = True
                    pygame.draw.circle(sc.screen, cl.RED, (check_x, check_y), 2)
                    break

        return distance

    def draw_rays(self, objects, foods):
        num_rays = 64
        angle_gap = 360 / num_rays
        self.n_rays = 0
        for i in range(num_rays):
            angle = math.radians(i * angle_gap)
            distance = self.cast_ray( angle, objects)
            end_x = self.x + math.cos(angle) * distance
            end_y = self.y + math.sin(angle) * distance
            if(self.calculate_vision_food(foods, self.x, self.y, end_x, end_y)):
                ray_color= cl.BLUE
                self.n_rays += 1
            else:
                ray_color= cl.WHITE
            pygame.draw.line(sc.screen, ray_color , (self.x, self.y), (end_x, end_y))

    def calculate_vision_food(self, foods, x1, y1, x2, y2):
        for food in foods:
            cx, cy = food.x, food.y
            px, py, is_within_segment  = self.ponto_proximo_reta(cx, cy, x1, y1, x2, y2)
        
            # Calcula a distância do ponto mais próximo ao centro do círculo
            distancia = math.sqrt((px - cx)**2 + (py - cy)**2)
            if distancia <= food.radius and is_within_segment:
                return True
        return False
    
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
