from mesa import Agent


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction chosen from one of eight directions
    """

    def __init__(self, unique_id, model, initialPosition, destination):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.pos = initialPosition
        self.destination = destination
        self.isMoving = False
        self.direction = [0, 0]

    def move(self):
        self.model.grid.move_agent(
            self, (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
        )
        self.setDirection()
        # TODO : Get if there is a traffic light near the car

    def setDirection(self):
        contents = self.model.grid.get_cell_list_contents([self.pos])
        road = [r for r in contents if isinstance(r, Road)][0]
        self.direction = road.direction

    def getRoads(self):
        possible_boxes = self.model.grid.get_neighborhood(self.pos, False, False)
        roads = []
        for cell in possible_boxes:
            contents = self.model.grid.get_cell_list_contents([cell])
            road = [r for r in contents if isinstance(r, Road)]
            roads = roads + road
        return roads

    def step(self):
        if not self.isMoving:
            road = self.getRoads()
            self.model.grid.move_agent(self, road[0].pos)
            self.setDirection()
            self.isMoving = True
            return
        self.move()


class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """

    def __init__(self, unique_id, model, state=False, timeToChange=10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass


class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """

    def __init__(self, unique_id, model, direction=[0, 0]):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
