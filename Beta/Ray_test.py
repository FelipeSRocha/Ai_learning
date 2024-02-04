import pygame
import math

# Inicializa o PyGame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Posição inicial do agente e velocidade
agent_x, agent_y = screen_width // 2, screen_height // 2
agent_speed = 5

# Bloco de comida
food_position = (100, 100)

# Paredes (x, y, largura, altura)
walls = [
    pygame.Rect(300, 300, 200, 50),
    pygame.Rect(50, 500, 200, 50),
]

clock = pygame.time.Clock()

def cast_ray(start_pos, angle, objects):
    x, y = start_pos
    sin_angle, cos_angle = math.sin(angle), math.cos(angle)
    distance = 0
    hit = False

    while not hit and distance < 200:
        distance += 1
        check_x, check_y = x + cos_angle * distance, y + sin_angle * distance
        
        for obj in objects:
            if obj.collidepoint((check_x, check_y)):
                hit = True
                pygame.draw.circle(screen, RED, (check_x, check_y), 2)
                break

    return distance

def draw_rays(screen, start_pos, objects):
    num_rays = 64
    angle_gap = 360 / num_rays

    for i in range(num_rays):
        angle = math.radians(i * angle_gap)
        distance = cast_ray(start_pos, angle, objects)
        end_x = start_pos[0] + math.cos(angle) * distance
        end_y = start_pos[1] + math.sin(angle) * distance
        pygame.draw.line(screen, WHITE, start_pos, (end_x, end_y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verifica entradas do teclado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        agent_x -= agent_speed
    if keys[pygame.K_RIGHT]:
        agent_x += agent_speed
    if keys[pygame.K_UP]:
        agent_y -= agent_speed
    if keys[pygame.K_DOWN]:
        agent_y += agent_speed
    if keys[pygame.K_ESCAPE]:
        running = False

    screen.fill(0)

    # Desenha paredes e comida
    # for wall in walls:
    #     pygame.draw.rect(screen, RED, wall)
    pygame.draw.circle(screen, GREEN, food_position, 10)

    # Desenha o agente
    pygame.draw.circle(screen, WHITE, (agent_x, agent_y), 10)

    # Desenha raios de visão
    objects = walls.copy()
    draw_rays(screen, (agent_x, agent_y), objects)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
