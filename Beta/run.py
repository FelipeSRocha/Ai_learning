import Env as e
import agent
from screen import screen
import scenery as sc

map = e.Ambiente(screen)

agente = agent.Agente((100,100),map.screen, 5, 5)
food = sc.Food((50,50),map.screen, 20)

map.add_agente(agente)
map.add_food_item(food)
map.add_scenery_item(sc.Wall(map.screen, (300,300), (50, 200)))
map.add_scenery_item(sc.Wall(map.screen, (100,200), (200, 200)))

map.run()
