from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid

from car import Car


class Mobility(Model):
    def __init__(self, height=50, width=50):
        self.schedule = SimultaneousActivation(self)
        self.grid = Grid(height, width, torus=True)

        car = Car((25, 25), self)
        self.grid.place_agent(car, (25, 25))
        self.schedule.add(car)
        self.running = True

    def step(self):
        self.schedule.step()
