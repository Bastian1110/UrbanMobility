from mesa import Agent
import random


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
        print(f"X {self.destination[0]} Y {self.destination[1]}")

    def move(self):
        home = self.lookForGoal()
        if home:
            self.model.grid.move_agent(self,self.destination)
            return
        trafficLigt = self.lookForLights()
        if not trafficLigt[0]:
            carsNear = self.lookForCars()
            if not carsNear:
                self.model.grid.move_agent(
                    self,
                    (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]),
                )
                self.setDirection()
                return
            return
        if trafficLigt[0]:
            if trafficLigt[1]:
                self.model.grid.move_agent(
                    self,
                    (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]),
                )
                self.setDirection()
                return
            if not trafficLigt[1]:
                return

    def lookForLights(self):
        posiblePosition = (
            self.pos[0] + self.direction[0],
            self.pos[1] + self.direction[1],
        )
        contents = self.model.grid.get_cell_list_contents([posiblePosition])
        trafficLight = [t for t in contents if isinstance(t, Traffic_Light)]
        if len(trafficLight) == 1:
            return [True, trafficLight[0].state]
        return [False, False]

    def lookForCars(self):
        posiblePositions = [
            (
                self.pos[0] + (self.direction[0]),
                self.pos[1] + (self.direction[1]),
            ),
            (
                self.pos[0] + (2 * self.direction[0]),
                self.pos[1] + (2 * self.direction[1]),
            ),
        ]
        for position in posiblePositions:
            if position[0] >= self.model.width or position[1] >= self.model.height:
                return False
                break
            contents = self.model.grid.get_cell_list_contents([position])
            nearCar = [c for c in contents if isinstance(c, Car)]
            if len(nearCar) == 1:
                return True
                break
        return False

    def setDirection(self):
        contents = self.model.grid.get_cell_list_contents([self.pos])
        trafficLigth = [t for t in contents if isinstance(t, Traffic_Light)]
        if len(trafficLigth) == 1:
            self.direction = self.direction
            return
        road = [r for r in contents if isinstance(r, Road)][0]
        if road.type == "f":
            self.direction = road.direction
            return
        position = self.pos
        direccionX = -1 if (self.destination[0] - 1 - self.pos[0] < 0) else 1
        direccionY = -1 if (self.destination[1] - 1 - self.pos[1] < 0) else 1
        if road.type == "R":
            if direccionX > 0 and direccionY > 0:
                self.direction = road.direction
                return
            if direccionX > 0 and direccionY < 0:
                self.direction = self.direction
                return
        if road.type == "r":
            if direccionX > 0 and direccionY < 0:
                self.direction = road.direction
                return
            else:
                self.direction = self.direction
                return
        if road.type == "L":
            if direccionX < 0 and direccionY > 0:
                self.direction = road.direction
                return
            if direccionX > 0 and direccionY < 0:
                self.direction = self.direction
                return
        if road.type == "l":
            if direccionX < 0 and direccionY < 0:
                self.direction = road.direction
                return
            else:
                self.direction = self.direction
                return
        if road.type == "P":
            if direccionX > 0 and direccionY > 0 and self.destination[1] > 1:
                self.direction = road.direction
                return
            if direccionX > 0 and direccionY < 0:
                self.direction = self.direction
                return
        if road.type == "p":
            if direccionX < 0 and direccionY > 0 and self.destination[1] > 1:
                self.direction = road.direction
                return
            else:
                self.direction = self.direction
                return
        if road.type == "N":
            if direccionX > 0 and direccionY < 0 and self.destination[1] < self.model.height - 1:
                self.direction = road.direction
                print(self.model.height-1)
                print(self.destination[1])
                return
            if direccionX > 0 and direccionY > 0:
                self.direction = self.direction
                return
        if road.type == "n":
            if direccionX < 0 and direccionY < 0 and self.destination[1] < self.model.height - 2:
                print(self.model.height-1)
                print(self.destination[1])
                self.direction = road.direction
                return
            else:
                self.direction = self.direction
                return

    def getRoads(self):
        possible_boxes = self.model.grid.get_neighborhood(self.pos, False, False)
        roads = []
        for cell in possible_boxes:
            contents = self.model.grid.get_cell_list_contents([cell])
            road = [r for r in contents if isinstance(r, Road)]
            roads = roads + road
        return roads
    
    def lookForGoal(self):
        position = self.pos
        possible_destination = self.model.grid.get_neighborhood(position, False, False)
        if self.destination in possible_destination:
            return True
        else:
            return False

    def step(self):
        if not self.isMoving:
            road = self.getRoads()
            self.model.grid.move_agent(self, road[0].pos)
            self.setDirection()
            self.isMoving = True
            return
        if self.pos == self.destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.move()


class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """

    def __init__(self, unique_id, loc, model, state=False, timeToChange=10):
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
        self.pos = loc
        self.partner = self
        self.opposingLight = self
        self.direction = ()
        self.firstStep = True
        self.cars = 0
        self.asked = False
        self.counter = self.timeToChange
        
    def calculateCars(self):
        cars = 0
        for i in range(6):
            x = self.pos[0] + ((i+1)*self.direction[0])
            y = self.pos[1] + ((i+1)*self.direction[1])
            if x < 0 or x > 21:
                break
            content = self.model.grid.get_cell_list_contents([(x,y)])
            possible_car = [r for r in content if isinstance(r, Car)]
            if len(possible_car) > 0:
                cars = cars + 1

        self.cars = cars
            
    def askTochange(self):
        cars1 = self.cars
        cars2 = self.opposingLight.cars
        if cars1 > cars2:
            self.state = True
            self.partner.state = True
            self.opposingLight.state = False
            self.opposingLight.partner.state = False
            self.asked = True
            self.partner.asked = True
            self.opposingLight.asked = True
            self.opposingLight.partner.asked = True
        elif cars2 > cars1:
            self.state = False
            self.partner.state = False
            self.opposingLight.state = True
            self.opposingLight.partner.state = True
            self.asked = True
            self.partner.asked = True
            self.opposingLight.asked = True
            self.opposingLight.partner.asked = True
        elif cars1 == 0 and cars2 == 0:
            pass
        elif cars2 == cars1:
            option = random.randint(0,2)
            if option == 0:
                self.state = True
                self.partner.state = True
                self.opposingLight.state = False
                self.opposingLight.partner.state = False               
            else:
                self.state = False
                self.partner.state = False
                self.opposingLight.state = True
                self.opposingLight.partner.state = True
            self.asked = True
            self.partner.asked = True
            self.opposingLight.asked = True
            self.opposingLight.partner.asked = True


    def direccionDeLuz(self):
        neighborhood = self.model.grid.get_neighborhood(self.pos , False, False)
        horizontal = False
        vertical = False
        if len(neighborhood) == 4 or len(neighborhood) == 3:
            n = 0
            for cell in neighborhood:
                content = self.model.grid.get_cell_list_contents([cell])
                rd = [r for r in content if isinstance(r, Road)]
                if len(rd) > 0:
                    if n == 0:
                        horizontal = True
                    if n == 1:
                        vertical = True
                n = n + 1
        
        
        direc0 = self.pos[0] - self.opposingLight.pos[0]
        direc1 = self.pos[1] - self.opposingLight.pos[1]

        
        if direc1 > 0 and direc0 > 0 and horizontal:
            self.direction = (1,0)
        elif direc1 > 0 and direc0 > 0 and vertical:
            self.direction = (0,1)
        elif direc1 > 0 and direc0 < 0 and vertical:
            self.direction = (0,1)
        elif direc1 > 0 and direc0 < 0 and horizontal:
            self.direction = (-1,0)
        elif direc1 < 0 and direc0 > 0 and horizontal:
            self.direction = (1,0)
        elif direc1 < 0 and direc0 > 0 and vertical:
            self.direction = (0,-1)
        elif direc1 < 0 and direc0 < 0 and horizontal:
            self.direction = (-1,0)
        elif direc1 < 0 and direc0 < 0 and vertical:
            self.direction = (0,-1) 


        

    def lookForOpposingLight(self):
        neighborhood = self.model.grid.get_neighborhood(self.pos,True,False)
        #print(self.pos)
        #print(neighborhood)
        for cell in neighborhood:
             content = self.model.grid.get_cell_list_contents([cell])
             traffic = [r for r in content if isinstance(r, Traffic_Light)]
             if len(traffic) == 1:
                #print(traffic[0].pos)
                if traffic[0] != self.partner and traffic[0].pos!= self.pos:
                    self.opposingLight = traffic[0]

    def lookForPartnerLight(self):
        position = (self.pos)
        
        neighborhood = self.model.grid.get_neighborhood(self.pos , False, False)
        #print(neighborhood)
        for cell in neighborhood:
            
            content = self.model.grid.get_cell_list_contents([cell])
            traffic = [r for r in content if isinstance(r, Traffic_Light)]
            if len(traffic) == 1:
                self.partner = traffic[0]

                
        

    def step(self):
        if self.firstStep:
            if self.opposingLight.pos == self.pos or self.opposingLight.pos == self.partner.pos:
                self.opposingLight = self.partner.opposingLight
            self.firstStep = False
            self.direccionDeLuz()
            print(self.pos)
            print(self.partner.pos)
            print(self.opposingLight.pos)
            print(self.direction)
            print()
        
        self.calculateCars()
        if self.asked and self.counter == 0:
            self.asked = False
            self.counter = self.timeToChange
        if not(self.asked):
            self.askTochange()
        if self.asked:
            self.counter = self.counter - 1


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

    def __init__(self, unique_id, model, type, direction=[0, 0]):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction
        self.type = type

    def step(self):
        pass
