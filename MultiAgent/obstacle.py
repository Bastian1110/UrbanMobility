from mesa import Agent


class Obstacle(Agent):
    def __init__(self, pos, model, size):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.h, self.w = size
