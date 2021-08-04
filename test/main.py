import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
import flask
from testdata import TestData

from models.model9 import model, data_index

app = flask.Flask(__name__)

dt = 0.1

U = np.array([[0]])
Z = np.array([[0]])

td = TestData()
f, F, h, H, X, P, Q, R, _ = model(td,dt)

z = []
z_press_capt = []
vz = []
vz_press_capt = []
az = []
az_capt = []
p = []
p_capt = []
Xs = []
Ps = []

fig = plt.figure()
axs = []
for i in range(6):
    axs.append(fig.add_subplot(2,3,i+1))

@app.route("/",methods=['POST'])
def index():
    global U,Z,X,F,f,P,Q,R,H,h,Xs,z,z_press_capt,vz,vz_press_capt,az,az_capt,p,p_capt,Ps,dt
    data = flask.request.get_json(force=True)
    U = np.array([[data["acc"][2]]])
    Z = np.array([[data["press"]]])

    Xkkm = f(X,U)
    Pkkm = F(X,U)@P@F(X,U).transpose() + Q
    v = Z - h(Xkkm)
    S = H(Xkkm)@Pkkm@H(Xkkm).transpose() + R
    K = Pkkm@H(Xkkm).transpose()@np.linalg.inv(S)
    X = Xkkm + K@v
    P = Pkkm - K@H(Xkkm)@Pkkm

    ##Save data
    Xs.append(X.tolist())
    Ps.append(P.tolist())

    #az.append(td.az)
    #az_capt.append(td.az_capt)

    az_capt.append(data["acc"][2])
    p_capt.append(data["press"])

    #z.append(td.z)
    z_press_capt.append(td.ptoz(p_capt[-1]))

    #vz.append(td.vz)
    if len(p_capt) < 2:
        vz_press_capt.append(0)
    else:
        vz_press_capt.append((td.ptoz(p_capt[-1]) - td.ptoz(p_capt[-2]))/dt)

    #p.append(td.p)
    #p_capt.append(td.p_capt)

    #td.update()

    return "", 200


def animate(i):
    global U,Z,X,F,f,P,Q,R,H,h,Xs,z,z_press_capt,vz,vz_press_capt,az,az_capt,p,p_capt,Ps,dt,axs

    if len(Xs) == 0:
        return

    timewindow = 10

    nbpoints = int(timewindow/dt)

    Xsarr = np.array(Xs[-nbpoints:])
    Psarr = np.array(Ps[-nbpoints:])
    z_press_capt_arr = z_press_capt[-nbpoints:]
    vz_press_capt_arr = vz_press_capt[-nbpoints:]
    az_capt_arr = az_capt[-nbpoints:]
    z_arr = z[-nbpoints:]
    vz_arr = vz[-nbpoints:]
    az_arr = az[-nbpoints:]
    p_arr = p[-nbpoints:]
    p_capt_arr = p_capt[-nbpoints:]

    time = np.array(list(range(len(Xs))))[-nbpoints:]*dt

    for ax in axs:
        ax.clear()

    ax = axs[0]
    if len(z_press_capt_arr) == len(time) : ax.plot(time, z_press_capt_arr, label="From pressure")
    if "z" in data_index : ax.plot(time, Xsarr[:,data_index["z"],0], label="Kalman")
    if len(z_arr) == len(time) : ax.plot(time, z_arr, label='True')
    ax.legend()
    ax.set_title("Altitude")

    ax = axs[1]
    if len(vz_press_capt_arr) == len(time) : ax.plot(time, vz_press_capt_arr, label="From pressure")
    if "vz" in data_index : ax.plot(time, Xsarr[:,data_index["vz"],0], label="Kalman")
    if len(vz_arr) == len(time) : ax.plot(time, vz_arr, label='True')
    ax.legend()
    ax.set_title("Vertical speed")

    ax = axs[2]
    if len(az_capt_arr) == len(time) : ax.plot(time, az_capt_arr, label="Measurements")
    if "az" in data_index : ax.plot(time, Xsarr[:,data_index["az"],0], label="Kalman")
    if "g" in data_index : ax.plot(time, Xsarr[:,data_index["g"],0], label="Gravty")
    if len(az_arr) == len(time) : ax.plot(time, az_arr, label="True")
    ax.legend()
    ax.set_title("Vertical acceleration")

    ax = axs[3]
    if len(p_capt_arr) == len(time) : ax.plot(time, p_capt_arr, label="Measurements")
    if "Pint" in data_index : ax.plot(time, Xsarr[:,data_index["Pint"],0], label="Kalman Inner Pressure")
    if "Pext" in data_index : ax.plot(time, Xsarr[:,data_index["Pext"],0], label="Kalman Outer Pressure")
    if len(p_arr) == len(time) : ax.plot(time, p_arr, label="True")
    ax.legend()
    ax.set_title("Pressure")

    ax = axs[4]
    if "z" in data_index : ax.plot(time, np.sqrt(Psarr[:,data_index["z"],data_index["z"]]))
    ax.set_title("Altitude standard dev")

    ax = axs[5]
    if "vz" in data_index : ax.plot(time, np.sqrt(Psarr[:,data_index["vz"],data_index["vz"]]))
    ax.set_title("Vertical speed standard dev")


if __name__ == "__main__":
    threading.Thread(
        target = app.run,
        args=("0.0.0.0", 7998)
    ).start()

    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()
