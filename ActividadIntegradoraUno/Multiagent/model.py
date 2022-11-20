from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from box import Box
from robot import Robot


class robotModel(Model):
    def __init__(self, nCajas, nRobots, width, height):
        super().__init__()
        self.numcajas = nCajas
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.actualStorage = (0,0)
        self.StorageList = []
        self.StorageList.append(self.actualStorage)
        self.index = 0
        self.running = True 

        #Crear robots
        for i in range(nRobots):
            robot = Robot(self.next_id(), self)
            self.schedule.add(robot)

            self.grid.place_agent(robot, (1,1))

        lugarCajas = self.random.sample(list(self.grid.coord_iter()),self.numcajas)

        for i in lugarCajas:
            if self.grid.is_cell_empty((i[1],i[2])):
                caja = Box(self.next_id(),(i[1],i[2]), self,show=True)

                self.grid.place_agent(caja, (i[1],i[2]))

    def step(self):
        self.schedule.step()