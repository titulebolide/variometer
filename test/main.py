import random
import matplotlib.pyplot as plt
import numpy as np

class TestData:
    def __init__(self):
        self.z = 1000
        self.zmin = 500
        self.zmax = 1500
        self.vz = 0
        self.vzmin = -10
        self.vzmax = 10
        self.az = 0
        self.az_capt = self.az
        self.dt = 1/10
        self.p = self.ztop(self.z)
        self.p_capt = self.p
        self.az_capt_std_dev = 0.1
        self.p_capt_std_dev = 3

    def walls(self,t):
        return ((t-0.5)*2)**3

    def ztop(self,z, tsea = 288):
        return 101325*np.exp(-0.02897*9.81*z/8.314/tsea)

    def ptoz(self,p, tsea = 288):
        return - 8.314*tsea/0.02897/9.81*np.log(p/101325)

    def update(self):
        daz = random.random() - 0.5 - 0.1*self.walls((self.z-self.zmin)/(self.zmax-self.zmin))
        daz = daz - self.az*0.2 - 0.05*self.walls((self.vz-self.vzmin)/(self.vzmax-self.vzmin))
        self.az = self.az + self.dt*daz
        self.vz = self.vz + self.dt*self.az
        self.z = self.z + self.dt*self.vz
        self.p = self.ztop(self.z)
        self.p_capt = self.p_capt + self.dt*(self.p - self.p_capt) + np.random.normal(scale = self.p_capt_std_dev)
        self.az_capt = self.az + np.random.normal(scale = self.az_capt_std_dev)

td = TestData()

from models.model9 import model, data_index

f, F, h, H, X, P, Q, R, get_U_Z = model(td)

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

time = np.arange(1,600,1/10)



for t in time:
    ## Kalman
    U,Z = get_U_Z(td)

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

    z.append(td.z)
    z_press_capt.append(td.ptoz(td.p_capt))

    vz.append(td.vz)
    if len(p_capt) == 0:
        vz_press_capt.append(0)
    else:
        vz_press_capt.append((td.ptoz(td.p_capt) - td.ptoz(p_capt[-1]))/td.dt)

    az.append(td.az)
    az_capt.append(td.az_capt)

    p.append(td.p)
    p_capt.append(td.p_capt)

    td.update()

Xs = np.array(Xs)
Ps = np.array(Ps)

plt.subplot(231)
plt.plot(time, z_press_capt, label="From pressure")
if "z" in data_index : plt.plot(time, Xs[:,data_index["z"],0], label="Kalman")
plt.plot(time, z, label='True')
plt.legend()
plt.title("Altitude")

plt.subplot(232)
plt.plot(time, vz_press_capt, label="From pressure")
if "vz" in data_index : plt.plot(time, Xs[:,data_index["vz"],0], label="Kalman")
plt.plot(time, vz, label='True')
plt.legend()
plt.title("Vertical speed")

plt.subplot(233)
plt.plot(time, az_capt, label="Measurements")
if "az" in data_index : plt.plot(time, Xs[:,data_index["az"],0], label="Kalman")
plt.plot(time, az, label="True")
plt.legend()
plt.title("Vertical acceleration")

plt.subplot(234)
plt.plot(time, p_capt, label="Measurements")
if "Pint" in data_index : plt.plot(time, Xs[:,data_index["Pint"],0], label="Kalman Inner Pressure")
if "Pext" in data_index : plt.plot(time, Xs[:,data_index["Pext"],0], label="Kalman Outer Pressure")
plt.plot(time, p, label="True")
plt.legend()
plt.title("Pressure")

plt.subplot(235)
if "z" in data_index : plt.plot(time, np.sqrt(Ps[:,data_index["z"],data_index["z"]]))
plt.title("Altitude standard dev")

plt.subplot(236)
if "vz" in data_index : plt.plot(time, np.sqrt(Ps[:,data_index["vz"],data_index["vz"]]))
plt.title("Vertical speed standard dev")
plt.show()
