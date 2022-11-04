def portrayalCar(car):
    assert car is not None
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": car.x,
        "y": car.y,
        "Color": "black",
    }


def portrayalObstacle(obstacle):
    assert obstacle is not None
    return {
        "Shape": "rect",
        "w": obstacle.w,
        "h": obstacle.h,
        "Filled": "true",
        "Layer": 0,
        "x": obstacle.x,
        "y": obstacle.y,
        "Color": "blue",
    }
