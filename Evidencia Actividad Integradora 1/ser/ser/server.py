import mesa
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid


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
        self.obj_x = model.actualStorage[0]
        self.obj_y = model.actualStorage[1]

    def step(self):
        if not(self.cajas):
            self.move()
            self.grab_box()
        elif self.cajas:
            if self.pos == (self.obj_x + 1,self.obj_y):
                self.place_box()
            else:
               self.move_goal()
               if self.pos == (self.obj_x + 1,self.obj_y):
                    self.place_box()
        

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, False, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        robot = [obj for obj in position if isinstance(obj, Robot)]
        if len(robot) < 1:
            self.model.grid.move_agent(self, chosen_step)

    def move_goal(self):
        position = self.pos
        #print(position[0])
        #print(position[1])
        #if position[0] > self.obj_x + 1 or position[0] < self.obj_x + 1:
        #    if position[0] > self.obj_x + 1:
        #        needed_step = self.model.grid.get_cell_list_contents([(position[0]-1,position[1])])
        #        possible_steps = self.model.grid.get_neighborhood(self.pos, False, True)
        #        if len(needed_step) < 1:
        #            self.model.grid.move_agent(self,(position[0]-1,position[1]))
        #            self.model.grid.move_agent(self.caj,(position[0]-1,position[1]))
        #    else:
        #        needed_step = self.model.grid.get_cell_list_contents([(position[0]+1,position[1])])
        #        possible_steps = self.model.grid.get_neighborhood(self.pos, False, True)
        #        if len(needed_step) < 1:
        #            self.model.grid.move_agent(self,(position[0]+ 1,position[1]))
        #            self.model.grid.move_agent(self.caj,(position[0]+1,position[1]))
        #    
        #elif position[1] > self.obj_y:
        #    needed_step = self.model.grid.get_cell_list_contents([(position[0],position[1]-1)])
        #    if len(needed_step) < 1:
        #        self.model.grid.move_agent(self,(position[0],position[1]-1))
        #        self.model.grid.move_agent(self.caj,(position[0],position[1]-1))
        if position[0] != self.model.actualStorage[0] + 1:
            direccion = self.model.actualStorage[0] - position[0] 
            self.model.grid.move_agent(self,(position[0]-1 if direccion < 0 else position[0] + 1,position[1]))
            self.model.grid.move_agent(self.caj,(position[0]-1 if direccion < 0 else position[0] + 1,position[1]))
        elif (position[1] != self.model.actualStorage[1]):
            direccion = self.model.actualStorage[1] - position[1] 
            self.model.grid.move_agent(self,(position[1]-1 if direccion < 0 else position[1] + 1,position[1]))
            self.model.grid.move_agent(self.caj,(position[1]-1 if direccion < 0 else position[1] + 1,position[1]))


        

    def grab_box(self):
        possible_boxes = self.model.grid.get_neighborhood(self.pos, False, True)
        print(possible_boxes)
        for obj in possible_boxes:
            print(obj)
            obj2 = self.model.grid.get_cell_list_contents([obj])
            C = [obj3 for obj3 in obj2 if isinstance(obj3, Caja)]
            if len(C) > 0 and obj != self.model.actualStorage:
                caja_agarrada = self.random.choice(C)
                print("Encontro caja")
                self.caj = caja_agarrada
                self.cajas = True
                self.model.grid.move_agent(self.caj,self.pos)
                break
            
    def place_box(self):
        boxes = self.model.grid.get_cell_list_contents([self.model.actualStorage])
        if len(boxes) < 5:
            self.model.grid.move_agent(self.caj,self.model.actualStorage)
            self.cajas = False
        else:
            self.model.actualStorage[1] += 1

class Caja(Agent):
    """
    Es una caja. Puede ser movida por un robot.
    """

    def __init__(self, pos, model,show=False):
        self.pos = pos
        self.show = show
    def step():
        pass

class robotModel(Model):
    """
    Crea un ambiente con 5 robots y un numero x de cajas
    """

    def __init__(self,nCajas,width,height):
        super().__init__()
        self.numcajas = nCajas
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.actualStorage = (0,0)

        #Crear robots
        for i in range(1):
            robot = Robot(self.next_id(), self)
            self.schedule.add(robot)

            self.grid.place_agent(robot, (1,1))

        lugarCajas = self.random.sample(list(self.grid.coord_iter()),self.numcajas)

        for i in lugarCajas:
            if self.grid.is_cell_empty((i[1],i[2])):
                caja = Caja((i[1],i[2]), self,show=True)

                self.grid.place_agent(caja, (i[1],i[2]))

    def step(self):
        self.schedule.step()

    pass

def cleaning_port(agent):
    # Función para crear el servidor, el Canvas, asignar el puerto de servidor,
    #   definir los colores y figuras de los agentes así como la asiganción de los valores para 
    #   crear Numero de Agentes, Espacio de habitación, Porcentaje de celdas sucias y tiempo de ejecución. 
    portrayal = {"Shape":"circle","Filled":"true", "r":0.5}

    # Diseño de los Agentes
    if type(agent) is Robot:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    
    # Diseño de la Dirt. 
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

grid = CanvasGrid(cleaning_port, 10, 10, 500, 500)
server = ModularServer(robotModel,[grid],"robotModel",{"nCajas":10,"width":10,"height":10})

server.port = 8521 
