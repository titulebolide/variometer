import flask
import numpy as np

buff = []
app = flask.Flask(__name__)

@app.route("/",methods=['POST'])
def index():
    global buff
    datas = flask.request.get_json(force=True)
    buff.extend(datas["data"])
    return "",200

@app.route("/save/",methods=['GET'])
def save():
    np.save("record.npy", buff)
    return "",200

app.run("0.0.0.0", 7998)
