from mesa import Agent


class Car(Agent):
    MOVE = 1

    def __init__(self, pos, model, rules, init_state=MOVE):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self._nextState = None

    def move(self):
        newx, newy = self.pos
        self.model.grid.move_agent(self, (newx + 1, newy + 1))

    def step(self):
        self._nextState = self.state
        self.move()

    def advance(self):
        self.state = self._nextState
