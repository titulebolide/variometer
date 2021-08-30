import numpy as np

def model(dt):
    alpha = 100/8
    beta = 2
    kappa = 1

    f = lambda X,U : np.array([
        [X[0,0] + dt*kappa*U[0,0]],
        [X[1,0] + dt*beta*(X[2,0] - X[1,0])],
        [X[2,0] - dt*alpha*X[0,0]]
    ])
    F = lambda X,U : np.array([
        [1, 0, 0],
        [0, 1-dt*beta, dt*beta],
        [-dt*alpha, 0, 1]
    ])
    h = lambda X : np.array([
        [X[1,0]]
    ])
    H = lambda X : np.array([
        [0,1,0]
    ])

    X = np.array([
        [0],
        [99730],
        [98730]
    ])
    Q = np.array([
        [0.0000001,0,0],
        [0,1.1,0],
        [0,0,1]
    ])**2

    P = np.copy(Q)
    R = np.array([
        [1]
    ])**2

    def get_U_Z(az, p):
        return np.array([[az]]),np.array([[p]])

    return f, F, h, H, X, P, Q, R, get_U_Z

data_index = {
    "vz" : 0,
    "Pint" : 1,
    "Pext" : 2,
}
