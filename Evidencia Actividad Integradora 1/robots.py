"""
Script de Agentes, Robot y Caja
Modelo del Medio Ambiente

Autores: Adrian Bravo López, Marco Barbosa Maruri

"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import Grid

class Robot(Agent):
    """
    Este es un robot, el robot puede moverse en las cuatro dirrecciones, puede levantar cajas 
    adjacentes en cuadricula y llevarcelas para hacer pilas de 5 cajas, su vision esta limitada a
    las cuatro celdas adjacentes en cuadricula lo cual significa que puede saber si un espacio esta
    ocupado o libre, finalmente el robot tambien puede saber si trae una caja.
    """
    def __init__(self,unique_id,model):
        super().__init__(unique_id, model)

    def step(self):
        self.move()
    

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, True, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        robot = [obj for obj in position if isinstance(obj, Robot)]
        if len(robot) < 1:
            self.model.grid.move_agent(self, chosen_step)

    def grab_box(self):

class Caja(Agent):
    """
    Es una caja. Puede ser movida por un robot.
    """
    def __init__(self,unique_id,model):

class Enviorment(Model):
    """
    Crea un ambiente con 5 robots y un numero 'X' de cajas.
    """
    def __init__(self):