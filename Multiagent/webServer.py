from flask import Flask, request, jsonify

from agent import *
from model import UrbanMobility


numberCars = 5
modelo = None
currentStep = 0

app = Flask("Urban Mobility")


@app.route("/init", methods=["POST", "GET"])
def initModel():
    global currentStep, modelo, numberCars

    if request.method == "POST":
        numberCars = int(request.form.get("NCars"))
        currentStep = 0

        modelo = UrbanMobility(numberCars, "base.txt")

        return jsonify({"message": "Parameters recieved, model initiated."})


@app.route("/getCars", methods=["GET"])
def getCars():
    global modelo

    if request.method == "GET":
        carsPositions = []
        for (a, x, z) in modelo.grid.coord_iter():
            for o in a:
                if isinstance(o, Car):
                    carsPositions.append(
                        {
                            "id": str(o.unique_id),
                            "x": x,
                            "y": 1,
                            "z": z,
                            "state": o.state,
                        }
                    )
        return jsonify({"positions": carsPositions})


@app.route("/getTrafficLights", methods=["GET"])
def getTrafficLights():
    global modelo

    if request.method == "GET":
        lights = []
        for (a, x, z) in modelo.grid.coord_iter():
            for o in a:
                if isinstance(o, Traffic_Light):
                    lights.append(
                        {
                            "id": str(o.unique_id),
                            "x": x,
                            "y": 1,
                            "z": z,
                            "state": o.state,
                        }
                    )
        return jsonify({"positions": lights})


@app.route("/update", methods=["GET"])
def updateModel():
    global currentStep, modelo
    if request.method == "GET":
        modelo.step()
        currentStep += 1
        return jsonify(
            {
                "message": f"Model updated to step {currentStep}.",
                "currentStep": currentStep,
            }
        )


if __name__ == "__main__":
    app.run(host="localhost", port=8080)
