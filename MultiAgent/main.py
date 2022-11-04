from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


from portrayal import portrayalCar
from model import Mobility


CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
RULES = "23/3"

# Make a world that is 50x50, on a 250x250 display.
canvas_element = CanvasGrid(portrayalCar, 50, 50, CANVAS_WIDTH, CANVAS_HEIGHT)

model_params = {
    "height": UserSettableParameter("slider", "Grid height", 50, 1, 100),
    "width": UserSettableParameter(
        "slider",
        "Grid width",
        50,
        1,
        100,
    ),
    "rules": RULES,
}

server = ModularServer(Mobility, [canvas_element], "Urban Mobility", model_params)

if __name__ == "__main__":
    server.launch()
