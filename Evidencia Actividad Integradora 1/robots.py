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
        self.cajas = False
        self.obj_x = 0
        self.obj_y = 0

    def step(self):
        if not(cajas):
            self.move()
            self.grab_box()
        else:
            if self.pos == [obj_x,obj_y]:
                place_box()
            else:
               self.move_goal()
               if self.pos == [obj_y,obj_x]:
                    place_box()

        


    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, False, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        robot = [obj for obj in position if isinstance(obj, Robot)]
        if len(robot) < 1:
            self.model.grid.move_agent(self, chosen_step)

    def move_goal(self):
        position = self.pos
        if position[0] > obj_x:
            needed_step = self.model.grid.get_cell_list_contents([position[0]-1,position[1]])
            if len(needed_step) < 1:
                self.model.grid.move_agent(self,[position[0]-1,position[1]])
                self.model.grid.move_agent(self.caj,[position[0]-1,position[1]])
            
        elif position[1] > obj_y:
            needed_step = self.model.grid.get_cell_list_contents([position[0],position[1]-1])
            if len(needed_step) < 1:
                self.model.grid.move_agent(self,[position[0],position[1]-1])
                self.model.grid.move_agent(self.caj,[position[0],position[1]-1])
        

    def grab_box(self):
        possible_boxes = self.model.grid.get_neighborhood(self.pos, False, True)
        for obj in possible_boxes:
            if isinstance(obj,Caja):
                self.caj = obj
                cajas = True
                self.model.grid.move_agent(caj,self.pos)
                break
    def place_box(self):
        boxes = self.model.grid.get_cell_list_contents([obj_x,obj_y])
        if boxes < 5:
            self.model.grid.move_agent(self.caj,[obj_x,obj_x])
            self.cajas = False
        else:
            self.obj_y = obj_y + 1

        
        