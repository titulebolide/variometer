import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
import flask
from testdata import TestData

from models.model9 import model, data_index

app = flask.Flask(__name__)

time = []
vz = []

@app.route("/",methods=['POST'])
def index():
    global time, vz
    data = flask.request.get_json(force=True)
    for d in data["Xs"]:
        time.append(d["timestamp"])
        vz.append(d["X"][0][0])

    return "", 200

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

def animate(i):
    global time, vz, ax

    ax.clear()
    ax.plot(time, vz)

if __name__ == "__main__":
    threading.Thread(
        target = app.run,
        args=("0.0.0.0", 7998)
    ).start()



    ani = animation.FuncAnimation(fig, animate, interval=1500)
    plt.show()
