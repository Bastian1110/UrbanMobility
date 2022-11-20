from flask import Flask, request, jsonify

from model import robotModel
from robot import Robot
from box import Box


numberRobots = 2
numberBoxes = 10
width = 10
height = 10
modelo = None
currentStep = 0

app = Flask("Robots vs Boxes")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, modelo, numberRobots, numberBoxes, width, height

    if request.method == 'POST':
        request_data = request.get_json()
        print(request_data)
        numberRobots = int(request_data["NRobots"])
        numberBoxes = int(request_data["NBoxes"])
        width = int(request_data["width"])
        height = int(request_data["height"])
        currentStep = 0

        modelo = robotModel(numberBoxes, numberRobots, width, height)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getRobots', methods=['GET'])
def getRobots():
    global modelo

    if request.method == 'GET':
        robotPositions = []
        for (a, x, z) in modelo.grid.coord_iter():
            for o in a:
                if isinstance(o, Robot):
                    robotPositions.append({"id": str(o.unique_id), "x": x, "y":1, "z":z})

        return jsonify({'positions': robotPositions})

@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    global modelo

    if request.method == 'GET':
        boxPositions = []
        for (a, x, z) in modelo.grid.coord_iter():
            for o in a:
                if isinstance(o, Box):
                    boxPositions.append({"id": str(o.unique_id), "x": x, "y":1, "z":z})

        return jsonify({'positions': boxPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, modelo
    if request.method == 'GET':
        modelo.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__ == '__main__':
    app.run(host="localhost", port=8080)