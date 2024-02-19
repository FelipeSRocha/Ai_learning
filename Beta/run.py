import Env as e
import agent
from screen import screen, screen_width, screen_height 
import scenery as sc

testing = False
num_episodes = 500
map = e.Ambiente(screen, testing, num_episodes)

agente = agent.Agente((100,100),map.screen, 25, 5)
food = sc.Food((50,50),map.screen, 50)

map.add_food_item(food)

# create 4 walls
map.add_scenery_item(sc.Wall(map.screen, (0,0), (1, screen_height)))
map.add_scenery_item(sc.Wall(map.screen, (0,0), (screen_width, 1)))
map.add_scenery_item(sc.Wall(map.screen, (screen_width-1,0), (1, screen_height)))
map.add_scenery_item(sc.Wall(map.screen, (0,screen_height-1), (screen_width, 1)))
# map.add_scenery_item(sc.Wall(map.screen, (100,200), (200, 200)))
map.add_agente(agente)

map.run()
