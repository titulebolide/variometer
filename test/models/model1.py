import numpy as np

def model(td,dt):
    f = lambda X,U : np.array([
        [X[0,0]]
    ])
    F = lambda X,U : np.array([
        [1]
    ])
    h = lambda X : np.array([
        [101325*np.exp(-0.02897*9.81*X[0,0]/8.314/288)]
    ])
    H = lambda X : np.array([
        [101325*-0.02897*9.81/8.314/288*np.exp(-0.02897*9.81*X[0,0]/8.314/288)]
    ])

    X = np.array([
        [1000]
    ])
    P = np.array([
        [10]
    ])**2
    Q = np.array([
        [10]
    ])**2
    R = np.array([
        [10]
    ])**2

    def get_U_Z(td):
        return np.array([[]]),np.array([[td.p_capt]])

    return f, F, h, H, X, P, Q, R, get_U_Z

data_index = {
    "z" : 0
}
