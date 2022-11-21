from mesa import Agent

class Box(Agent):
    def __init__(self, unique_id, pos, model, show=False):
        super().__init__(unique_id, model)
        self.pos = pos
        self.show = show
        self.grabbed = False

    def step(self):
        pass