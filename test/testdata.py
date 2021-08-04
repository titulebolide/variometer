import numpy as np
import random

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
