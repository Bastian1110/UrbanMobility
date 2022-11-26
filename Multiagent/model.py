from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json


class UrbanMobility(Model):
    """
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """

    def __init__(self, cars, city):

        dataDictionary = json.load(open("mapDictionary.json"))

        self.traffic_lights = []
        self.destinantions = []

        with open(city) as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0]) - 1
            self.height = len(lines)
            print(f"Width : {self.width}, Height : {self.height}")

            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(
                            f"r_{r*self.width+c}", self, "f", dataDictionary[col]
                        )
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in list("rRlLpPnN"):
                        agent = Road(
                            f"r_{r*self.width+c}", self, col, dataDictionary[col]
                        )
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(
                            f"tl_{r*self.width+c}",
                            self,
                            False if col == "S" else True,
                            int(dataDictionary[col]),
                        )
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinantions.append(agent)

        for i in range(cars):
            randomUbication = True
            randomDestination = True
            while randomDestination == randomUbication:
                randomUbication = self.random.choice(self.destinantions)
                randomDestination = self.random.choice(self.destinantions)
            agent = Car(f"c_{i}", self, randomUbication.pos, randomDestination.pos)
            self.grid.place_agent(agent, randomUbication.pos)
            self.schedule.add(agent)

        self.num_agents = cars
        self.running = True

    def step(self):
        """Advance the model by one step."""
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()
