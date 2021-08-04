import numpy as np

def model(td,dt):
    f = lambda X,U : np.array([
        [X[0,0] + dt*X[1,0]],
        [X[1,0] + dt*X[2,0]],
        [X[2,0]],
        [X[3,0]]
    ])
    F = lambda X,U : np.array([
        [1, dt,     0,0],
        [0,     1, dt,0],
        [0,     0,     1,0],
        [0,0,0,1]
    ])
    h = lambda X : np.array([
        [101325*np.exp(-0.02897*9.81*X[0,0]/8.314/288)+X[3,0]],
        [X[2,0]]
    ])
    H = lambda X : np.array([
        [101325*-0.02897*9.81/8.314/288*np.exp(-0.02897*9.81*X[0,0]/8.314/288), 0, 0, 1],
        [0,0,1,0]
    ])

    X = np.array([
        [1000],
        [0],
        [0],
        [0]
    ])
    P = np.array([
        [10,0,0,0],
        [0,2,0,0],
        [0,0,0.5,0],
        [0,0,0,10],
    ])**2
    Q = np.array([
        [10,0,0,0],
        [0,2,0,0],
        [0,0,0.5,0],
        [0,0,0,10],
    ])**2
    R = np.array([
        [10,0],
        [0,500]
    ])**2

    def get_U_Z(td):
        return np.array([[]]),np.array([[td.p_capt, td.az_capt]])

    return f, F, h, H, X, P, Q, R, get_U_Z

data_index = {
    "z" : 0,
    "vz" : 1,
    "az" : 2,
    "P1" : 3
}
