from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from caja import Caja
from robots import Robot

class robotModel(Model):
    """
    Crea un ambiente con 5 robots y un numero x de cajas
    """

    def __init__(self,nCajas,width,height):
        self.numcajas = nCajas
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        #Crear robots
        for i in range(5):
            robot = Robot(1, self)
            self.schedule.add(robot)

            self.grid.place_agent(robot, (1,1))

        lugarCajas = self.random.sample(list(self.grid.coord_iter()),self.numcajas)

        for i in lugarCajas:
            caja = Caja((i[1],i[2]), self,show=True)

            self.grid.place_agent(caja, (i[1],i[2]))

    def step(self):
        self.schedule.step()

    pass

