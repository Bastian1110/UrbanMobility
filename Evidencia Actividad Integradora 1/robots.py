"""
Script de Agentes, Robot y Caja
Modelo del Medio Ambiente

Autores: Adrian Bravo López, Marco Barbosa Maruri

"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import Grid

class Robot(Agent):
    """
    Este es un robot, el robot puede moverse en las cuatro dirrecciones, puede levantar cajas 
    adjacentes en cuadricula y llevarcelas para hacer pilas de 5 cajas, su vision esta limitada a
    las cuatro celdas adjacentes en cuadricula lo cual significa que puede saber si un espacio esta
    ocupado o libre, finalmente el robot tambien puede saber si trae una caja.
    """
    def __init__(self,unique_id,model):


class Caja(Agent):
    """
    Es una caja. Puede ser movida por un robot.
    """
    def __init__(self,unique_id,model):

class Enviorment(Model):
    """
    Crea un ambiente con 5 robots y un numero 'X' de cajas.
    """
    def __init__(self):