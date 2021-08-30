import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
import flask
from models.model9 import model, data_index

app = flask.Flask(__name__)

dt = 2/1000

U = np.array([[0]])
Z = np.array([[0]])

f, F, h, H, X, P, Q, R, _ = model(dt)

z_press_capt = []
vz_press_capt = []
az_capt = []
p_capt = []
Xs = []
Ps = []
time = []
time_p = []

current_press = False

use_file = True
file_name = 'record.npy'

def ptoz(p, tsea = 288):
    return - 8.314*tsea/0.02897/9.81*np.log(p/101325)

fig = plt.figure()
axs = []
for i in range(4):
    axs.append(fig.add_subplot(2,2,i+1))

if not use_file:
    @app.route("/",methods=['POST'])
    def index():
        datas = flask.request.get_json(force=True)
        for data in datas['data']:
            handle_data(data)
        return "", 200

def handle_data(data):
    global U,Z,X,F,f,P,Q,R,H,h,Xs,z_press_capt,vz_press_capt,az_capt,p_capt,Ps,current_press, time, time_p

    if "p" in data:
        time_p.append(data['ts'])
        p_capt.append(data['p'])
        z_press_capt.append(ptoz(data['p']))
        current_press = data["p"]

    elif "a" in data:
        time.append(data["ts"])
        az_capt.append(data["a"])
        U = np.array([[data["a"]]])

        Xkkm = f(X,U)
        Pkkm = F(X,U)@P@F(X,U).transpose() + Q
        if current_press != False:
            Z = np.array([[current_press]])
            v = Z - h(Xkkm)
            S = H(Xkkm)@Pkkm@H(Xkkm).transpose() + R
            K = Pkkm@H(Xkkm).transpose()@np.linalg.inv(S)
            X = Xkkm + K@v
            P = Pkkm - K@H(Xkkm)@Pkkm
        else:
            X = np.copy(Xkkm)
            P = np.copy(Pkkm)

        ##Save data
        Xs.append(X.tolist())
        Ps.append(P.tolist())

        if len(p_capt) < 2:
            vz_press_capt.append(0)
        else:
            vz_press_capt.append((ptoz(p_capt[-1]) - ptoz(p_capt[-2]))/(time_p[-1]-time_p[-2])*1000)

def animate(i):
    global U,Z,X,F,f,P,Q,R,H,h,Xs,z,z_press_capt,vz,vz_press_capt,az,az_capt,p,p_capt,Ps,axs,use_file

    if len(Xs) == 0:
        return

    time_arr = np.array(time)
    time_arr = time_arr[time_arr > time[-1]-10000]
    time_p_arr = np.array(time_p)
    time_p_arr = time_p_arr[time_p_arr > time_p[-1]-10000]

    nbpoints = len(time_arr)
    Xsarr = np.array(Xs[-nbpoints:])
    Psarr = np.array(Ps[-nbpoints:])
    vz_press_capt_arr = vz_press_capt[-nbpoints:]
    az_capt_arr = az_capt[-nbpoints:]

    nbpoints = len(time_p_arr)
    p_capt_arr = p_capt[-nbpoints:]

    for ax in axs:
        ax.clear()

    ax = axs[0]
    if len(vz_press_capt_arr) == len(time_arr) : ax.plot(time_arr, vz_press_capt_arr, label="From pressure")
    if "vz" in data_index : ax.plot(time_arr, Xsarr[:,data_index["vz"],0], label="Kalman")
    ax.legend()
    ax.set_title("Vertical speed")

    ax = axs[1]
    if len(az_capt_arr) == len(time_arr) : ax.plot(time_arr, az_capt_arr, label="Measurements")
    if "az" in data_index : ax.plot(time_arr, Xsarr[:,data_index["az"],0], label="Kalman")
    ax.legend()
    ax.set_title("Vertical acceleration")

    ax = axs[2]
    if len(p_capt_arr) == len(time_p_arr) : ax.plot(time_p_arr, p_capt_arr, label="Measurements")
    if "Pint" in data_index : ax.plot(time_arr, Xsarr[:,data_index["Pint"],0], label="Kalman Inner Pressure")
    if "Pext" in data_index : ax.plot(time_arr, Xsarr[:,data_index["Pext"],0], label="Kalman Outer Pressure")
    ax.legend()
    ax.set_title("Pressure")

    ax = axs[3]
    if "vz" in data_index : ax.plot(time_arr, np.sqrt(Psarr[:,data_index["vz"],data_index["vz"]]))
    ax.set_title("Vertical speed standard dev")


if __name__ == "__main__":
    if not use_file:
        threading.Thread(
            target = app.run,
            args=("0.0.0.0", 7998)
        ).start()
        ani = animation.FuncAnimation(fig, animate, interval=1500)

    else:
        datas = np.load(file_name, allow_pickle=True)
        for data in datas:
            handle_data(data)
        animate(0)

    plt.show()
