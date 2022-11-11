from mesa import Agent


class Car(Agent):
    MOVE = 1
    DIRECTIONS = {"N": [0, 1], "E": [1, 0], "S": [0, -1], "W": [1, 0]}

    def __init__(self, pos, model, init_state=MOVE):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state

    def move(self, direction):
        newx, newy = self.pos
        self.model.grid.move_agent(
            self,
            (
                newx + self.DIRECTIONS[direction][0],
                newy + self.DIRECTIONS[direction][1],
            ),
        )

    def step(self):
        self._nextState = self.state
        self.move("S")
