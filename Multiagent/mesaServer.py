from agent import *
from model import UrbanMobility
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 1, "w": 1, "h": 1}

    if isinstance(agent, Road):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0

    if isinstance(agent, Destination):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0

    if isinstance(agent, Traffic_Light):
        portrayal["Color"] = "red" if not agent.state else "green"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if isinstance(agent, Obstacle):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if isinstance(agent, Car):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    return portrayal


pathToCity = "base.txt"

with open(pathToCity) as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0]) - 1
    height = len(lines)

model_params = {"cars": 35, "city": pathToCity}

print(width, height)
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

server = ModularServer(UrbanMobility, [grid], "Traffic Base", model_params)

server.port = 8521  # The default
server.launch()
