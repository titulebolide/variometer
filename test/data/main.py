import json
import numpy as np
import matplotlib.pyplot as plt
with open("record_1630235207443.json", "r") as f:
    data = json.load(f)
X = []
for i in data["data"]:
    if "p" in i:
        X.append([i["ts"],i["p"]])
X.sort(key=lambda x : x[0])
X = np.array(X)
plt.plot(X[:,0],X[:,1])
plt.show()
