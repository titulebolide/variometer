import numpy as np

def model(td):
    alpha = 100/8
    beta = 1

    f = lambda X,U : np.array([
        [X[0,0] + td.dt*U[0,0]],
        [X[1,0] + td.dt*beta*(X[2,0] - X[1,0])],
        [X[2,0] - td.dt*alpha*X[0,0]]
    ])
    F = lambda X,U : np.array([
        [1, 0, 0],
        [0, 1-td.dt*beta, td.dt*beta],
        [-td.dt*alpha, 0, 1]
    ])
    h = lambda X : np.array([
        [X[1,0]]
    ])
    H = lambda X : np.array([
        [0,1,0]
    ])

    X = np.array([
        [1],
        [101325],
        [101325]
    ])
    P = np.array([
        [0.2,0,0],
        [0,10,0],
        [0,0,10]
    ])**2
    Q = np.array([
        [0.2,0,0],
        [0,10,0],
        [0,0,10]
    ])**2
    R = np.array([
        [10]
    ])**2

    def get_U_Z(td):
        return np.array([[td.az_capt]]),np.array([[td.p_capt]])

    return f, F, h, H, X, P, Q, R, get_U_Z

data_index = {
    "vz" : 0,
    "Pint" : 1,
    "Pext" : 2,
}
