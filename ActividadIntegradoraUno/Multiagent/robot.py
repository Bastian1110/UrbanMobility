from mesa import Agent


from box import Box

class Robot(Agent):
    """
    Este es un robot, el robot puede moverse en las cuatro dirrecciones, puede levantar cajas 
    adjacentes en cuadricula y llevarcelas para hacer pilas de 5 cajas, su vision esta limitada a
    las cuatro celdas adjacentes en cuadricula lo cual significa que puede saber si un espacio esta
    ocupado o libre, finalmente el robot tambien puede saber si trae una caja.
    """
    def __init__(self,unique_id,model):
        super().__init__(unique_id, model)
        self.cajas = False
        self.obj_x = model.actualStorage[0]
        self.obj_y = model.actualStorage[1]

    def step(self):
        if not(self.cajas):
            self.move()
            self.grab_box()
        elif self.cajas:
            objNeighboor = self.model.grid.get_neighborhood(self.model.actualStorage, False, False)
            if self.pos in objNeighboor:
                self.place_box()
            else:
               self.move_goal()
               if self.pos in objNeighboor:
                    self.place_box()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, False, True)
        chosen_step = self.random.choice(possible_steps)
        position = self.model.grid.get_cell_list_contents([chosen_step])
        robot = [obj for obj in position if isinstance(obj, Robot)]
        if len(robot) < 1:
            self.model.grid.move_agent(self, chosen_step)

    def move_goal(self):
        position = self.pos
        moved = False
        direccionX = -1 if (self.model.actualStorage[0] - position[0] < 0) else 1 
        direccionY = -1 if (self.model.actualStorage[1] - position[1] < 0) else 1 
        posibleCellX = (position[0] + direccionX , position[1])
        posibleCellY = (position[0], position[1] + direccionY)
        if position != self.model.actualStorage:
            if self.model.grid.is_cell_empty(posibleCellX) and position[0] != self.model.actualStorage[0]:
                self.model.grid.move_agent(self, posibleCellX)
                self.model.grid.move_agent(self.caj, posibleCellX)
            else:
                self.model.grid.move_agent(self, posibleCellY)
                self.model.grid.move_agent(self.caj, posibleCellY)
  

    def grab_box(self):
        possible_boxes = self.model.grid.get_neighborhood(self.pos, False, True)
        for obj in possible_boxes:
            obj2 = self.model.grid.get_cell_list_contents([obj])
            C = [obj3 for obj3 in obj2 if isinstance(obj3, Box)]
            state = True
            for cor in self.model.StorageList:
                if cor == obj:
                    state = False
            if len(C) > 0 and state:
                caja_agarrada = self.random.choice(C)
                self.caj = caja_agarrada
                self.cajas = True
                self.model.grid.move_agent(self.caj,self.pos)
                break
            
    def place_box(self):
        self.model.grid.move_agent(self.caj,self.model.actualStorage)
        self.cajas = False
        boxes = self.model.grid.get_cell_list_contents([self.model.actualStorage])
        if len(boxes) == 5:
            print("New Storage : ",(self.model.actualStorage[0], self.model.actualStorage[1] + 1))
            self.model.actualStorage = (self.model.actualStorage[0] + 1, self.model.actualStorage[1])
            self.model.index = self.model.index + 1
            self.model.StorageList.append(self.model.actualStorage)