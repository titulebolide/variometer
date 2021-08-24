import json
import numpy as np
import matplotlib.pyplot as plt
with open("record_1629800224591.json", "r") as f:
    data = json.load(f)
X = []
for i in data["data"]:
    if "acc" in i:
        X.append([i["ts"],i["acc"]])
X.sort(key=lambda x : x[0])
X = np.array(X)
plt.plot(X[:,0],X[:,1])
plt.show()
