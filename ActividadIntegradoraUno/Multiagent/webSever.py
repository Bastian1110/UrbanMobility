from flask import Flask, request, jsonify

from model import robotModel
from robot import Robot
from box import Box

width = 10
height = 10
model = None
currentStep = 0

app = Flask("Robots vs Boxes")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, model, number_agents, width, height

    if request.method == 'POST':
        print(request.form)
        numberRobots = int(request.form.get('NRobots'))
        numberBoxes = int(request.form.get('NBoxes'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 0

        print(request.form)
        print(number, width, height)
        model = robotModel(numberBoxes, numberRobots, width, height)

        return jsonify({"message":"Parameters recieved, model initiated."})
    if request.method == 'GET':
        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getRobots', methods=['GET'])
def getRobots():
    global model

    if request.method == 'GET':
        robotPositions = [{"id": str(a.unique_id), "x": x, "y":1, "z":z} for (a, x, z) in model.grid.coord_iter() if isinstance(a, Robot)]

        return jsonify({'positions': robotPositions})

@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    global model

    if request.method == 'GET':
        boxPositions = [{"id": str(a.unique_id), "x": x, "y":1, "z":z} for (a, x, z) in model.grid.coord_iter() if isinstance(a, Box)]

        return jsonify({'positions': boxPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, model
    if request.method == 'GET':
        model.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)