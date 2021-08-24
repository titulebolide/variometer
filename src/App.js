/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  Button,
  useColorScheme,
  View
} from 'react-native';

import { barometer, accelerometer, setUpdateIntervalForType, SensorTypes } from "react-native-sensors";

import { create, all } from 'mathjs'

import Tone from "react-native-tone-android";

import Share from 'react-native-share';


var RNFS = require('react-native-fs');


import RNDisableBatteryOptimizationsAndroid from 'react-native-disable-battery-optimizations-android';

RNDisableBatteryOptimizationsAndroid.isBatteryOptimizationEnabled().then((isEnabled)=>{
  if(isEnabled){
    RNDisableBatteryOptimizationsAndroid.openBatteryModal();
  }
});



const config = { }
const math = create(all, config)

//const dt = 0.01
const beta = 2
const alpha = 12 //100/8

setUpdateIntervalForType(SensorTypes.accelerometer, 2);
setUpdateIntervalForType(SensorTypes.barometer, 100);

class App extends React.Component {

  state = {
    vz:0,
    step:"Initializing",
    recordButtonText:"Start recording",
    infoText:"",
    lastRecordFile:false
  }

  //config
  doSendData = false //send data to TCP
  playTone = false // Plays beep beep
  runKalman = false // Run kalman iterations

  // record
  isRecording = false
  isHandlingRecordToggle = false
  recordBuffer = []

  // data to handle subscriptions
  subscriptions = []
  intervals = []

  // Kalman linked data
  acc = false
  press = false
  g_const = 0
  initial_p = 0
  runningState = 0 //0 for initializing, 1 for ending initializing, 2 for can begin
  nb_init_a = 0
  nb_init_p = 0
  stopTone = false
  lastTimestamp = 0
  Xs = []
  U = false
  Z = false
  X = false
  f = false
  F = false
  h = false
  H = false
  P = false
  Q = false
  R = false

  initKalman = () => {
    this.f = (X,U,dt) => math.matrix([
      [X.get([0,0]) + dt*0.3*U.get([0,0])],
      [X.get([1,0]) + dt*beta*(X.get([2,0]) - X.get([1,0]))],
      [X.get([2,0]) - dt*alpha*X.get([0,0])]
    ])

    this.F = (X,U,dt) => math.matrix([
      [1, 0, 0],
      [0, 1-dt*beta, dt*beta],
      [-dt*alpha, 0, 1]
    ])

    this.h = (X) => math.matrix([
      [X.get([1,0])]
    ])

    this.H = (X) => math.matrix([
      [0,1,0]
    ])

    this.X = math.matrix([
        [0],
        [this.initial_p],
        [this.initial_p]
    ])
    this.P = math.matrix([
        [0.2,0,0],
        [0,1,0],
        [0,0,1]
    ])
    this.P = math.square(this.P)
    this.Qdt = math.matrix([
        [400,0,0],
        [0, 100,0],
        [0,0,0.1]
    ])
    this.Qdt = math.square(this.Qdt)
    this.R = math.matrix([
        [400]
    ])
    this.R = math.square(this.R)

    this.U = math.matrix([[0]])
    this.Z = math.matrix([[this.initial_p]])
    if (this.playTone) {
      setTimeout(this.tonePlayer,1)
    }
    this.intervals.push(
      setInterval(this.printX, 100)
    )
    this.runningState = 2
  }

  kalmanIteration = () => {
    this.U.subset(math.index(0,0), this.acc.data)

    let dt = 0.01
    if (this.lastTimestamp !== 0) {
      dt = (this.acc.timestamp - this.lastTimestamp)/1000
    }
    this.lastTimestamp = this.acc.timestamp

    this.Q = math.multiply(dt*dt, this.Qdt)

    let Xkkm = this.f(this.X,this.U,dt)
    let Pkkm = math.add(
      math.multiply(
        math.multiply(
          this.F(this.X,this.U,dt),
          this.P
        ),
        math.transpose(this.F(this.X,this.U,dt))
      ),
      this.Q
    )

    if (this.press !== false) {
      this.Z.subset(math.index(0,0), this.press)

      let v = math.subtract(this.Z, this.h(Xkkm))
      let S = math.add(
        math.multiply(
          math.multiply(
            this.H(Xkkm),
            Pkkm
          ),
          math.transpose(this.H(Xkkm))
        ),
        this.R
      )
      let K = math.multiply(
        math.multiply(
          Pkkm,
          math.transpose(this.H(Xkkm))
        ),
        math.inv(S)
      )
      this.X = math.add(
        Xkkm,
        math.multiply(
            K,
            v
        )
      )
      this.P = math.subtract(
        Pkkm,
        math.multiply(
          math.multiply(
            K,
            this.H(Xkkm)
          ),
          Pkkm
        )
      )
      this.press = false
    } else {
      this.X = Xkkm
      this.P = Pkkm
    }
    this.Xs.push({
      timestamp:this.acc.timestamp,
      X : this.X._data
    })
  }

  printX = () => {
    this.setState({vz:this.X.get([0,0])})
  }

  sendData = () => {
    data = {
      Xs : this.Xs
    }
    this.Xs = []
    fetch(
      "http://192.168.43.241:7998/",
      {
        method: "POST",
        body: JSON.stringify(data),
        headers: "Content-Type: application/json"
      }
    ).catch((error) => {
      return
    });
  }

  tonePlayer = () => {
    let vz = this.X.get([0,0])
    let inter = 250 - 130*vz
    if (vz >= 0.1) {
      Tone.play(500 + 300*vz, inter)
    }
    if (this.stopTone) {
      this.stopTone = false
      return
    }
    setTimeout(this.tonePlayer,inter*2)
  }

  componentDidMount = () => {
    this.subscriptions.push(
      barometer.subscribe(({ pressure }) => {
        if(this.runningState == 2) {
          this.press = pressure*100
          if (this.isRecording) {
            this.recordBuffer.push({
              "ts" : Date.now(),
              "press" : pressure*100
            })
          }
        } else if (this.runningState == 0) {
          this.nb_init_p += 1
          this.initial_p += pressure*100
        }
      })
    )

    this.subscriptions.push(
      accelerometer.subscribe(({ x, y, z, timestamp }) => {
        if (this.runningState == 2) {
          this.acc = {
            timestamp : timestamp,
            data : Math.sqrt(x*x+y*y+z*z)-this.g_const
          }
          if (this.isRecording) {
            this.recordBuffer.push({
              "ts" : timestamp,
              "acc" : Math.sqrt(x*x+y*y+z*z)-this.g_const
            })
          }
          if (this.runKalman) {
            setTimeout(this.kalmanIteration,1)
          }
        } else if (this.runningState == 0) {
          this.nb_init_a += 1
          this.g_const += Math.sqrt(x*x+y*y+z*z)
          if (this.nb_init_a > 10 && this.nb_init_p > 10) {
            this.runningState = 1
            this.g_const /= this.nb_init_a
            this.initial_p /= this.nb_init_p
            if (this.runKalman) {
              this.initKalman()
            } else {
              this.runningState = 2
            }
            if (this.doSendData) {
              this.intervals.push(
                setInterval(this.sendData, 100)
              )
            }
            this.setState({step:"Running"})
          }
        }
      })
    )
  }

  componentWillUnmount = () => {
    for (sub of this.subscriptions) {
      sub.unsubscribe()
    }
    for (inter of this.intervals) {
      clearInterval(inter)
    }
  }

  toggleRecording = () => {
    if (this.isHandlingRecordToggle) return;
    this.isHandlingRecordToggle = true
    if (this.isRecording) {
      let path = RNFS.DocumentDirectoryPath + '/record_' + Date.now() + '.json'
      RNFS.writeFile(path, JSON.stringify({"data": this.recordBuffer}), 'utf8')
      .then((success) => {
        console.log('FILE WRITTEN!');
        this.recordBuffer = []
        this.setState({recordButtonText : "Start recording", infoText : "Saved at "+path, "lastRecordFile": path})
        this.isRecording = false;
        this.isHandlingRecordToggle = false;
      })
      .catch((err) => {Button
        console.log(err.message);
        this.isHandlingRecordToggle = false;
      });
    } else {
      this.setState({recordButtonText : "Stop recording"})
      this.isRecording = true;
      this.isHandlingRecordToggle = false;
    }
  }

  render = () => (
    <>
      <Text>
        {this.state.step}
      </Text>
      <Text>
        {this.state.vz}
      </Text>
      <Text>
        {this.U && this.U.get([0,0])}
      </Text>
      <Text>
        {this.Z && this.Z.get([0,0])}
      </Text>
      <Text>
        {this.P && this.P.get([0,0])}
      </Text>
      <Button  onPress={this.toggleRecording}  title={this.state.recordButtonText}/>
      <Text></Text>
      {this.state.lastRecordFile &&
        <Button
          onPress={() => Share.open({
              url: "file://"+this.state.lastRecordFile
          })}
          title={"Share last record \n (" + this.state.lastRecordFile + ")"}
        />
      }
    </>
  )
};

export default App;
