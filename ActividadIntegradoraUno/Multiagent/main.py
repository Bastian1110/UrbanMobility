from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import NumberInput

from robot import Robot
from model import robotModel


def cleaning_port(agent):
    # Función para crear el servidor, el Canvas, asignar el puerto de servidor,
    # definir los colores y figuras de los agentes así como la asiganción de los valores para 
    # crear Numero de Agentes, Espacio de habitación, Porcentaje de celdas sucias y tiempo de ejecución. 
    portrayal = {"Shape":"circle","Filled":"true", "r":0.5}

    # Diseño de los Agentes
    if type(agent) is Robot:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    
    # Diseño de las Cajas. 
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

model_params = {
    "nCajas" : NumberInput("miau", value=10),
    "width":10,
    "height":10
}

grid = CanvasGrid(cleaning_port, 10, 10, 500, 500)
server = ModularServer(robotModel,[grid],"Robot vs Boxes",model_params)

server.port = 8521 

if __name__ == "__main__":
    server.launch()