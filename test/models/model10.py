import numpy as np

def model(td,dt):
    alpha = 100/8
    beta = 1

    f = lambda X,U : np.array([
        [X[0,0] + dt*(U[0,0]-X[3,0])],
        [X[1,0] + dt*beta*(X[2,0] - X[1,0])],
        [X[2,0] - dt*alpha*X[0,0]],
        [X[3,0]]
    ])
    F = lambda X,U : np.array([
        [1, 0, 0, -dt],
        [0, 1-dt*beta, dt*beta,0],
        [-dt*alpha, 0, 1,0],
        [0,0,0,1]
    ])
    h = lambda X : np.array([
        [X[1,0]]
    ])
    H = lambda X : np.array([
        [0,1,0,0]
    ])

    X = np.array([
        [0],
        [84300],
        [84300],
        [9.81]
    ])
    P = np.array([
        [0.2,0,0,0],
        [0,10,0,0],
        [0,0,10,0],
        [0,0,0,0.1]
    ])**2
    Q = np.array([
        [0.2,0,0,0],
        [0,10,0,0],
        [0,0,10,0],
        [0,0,0,0.1]
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
    "g" : 3
}
