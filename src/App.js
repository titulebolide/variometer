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
  useColorScheme,
  View,
} from 'react-native';

import { barometer, accelerometer, setUpdateIntervalForType, SensorTypes } from "react-native-sensors";

import { create, all } from 'mathjs'

import Tone from "react-native-tone-android";

const config = { }
const math = create(all, config)

const dt = 0.1
const beta = 1
const alpha = 100/8

setUpdateIntervalForType(SensorTypes.accelerometer, dt*1000);
setUpdateIntervalForType(SensorTypes.barometer, dt*1000);

class App extends React.Component {

  state = {vz:0, step:"Initializing"}
  sendData = true
  acc = [0,0,0]
  press = 0
  g_const = 0
  initial_p = 0
  runningState = 0 //0 for initializing, 1 for ending initializing, 2 for can begin
  nb_init_a = 0
  nb_init_p = 0
  playTone = true
  subscriptions = []
  intervals = []
  stopTone = false
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
    this.f = (X,U) => math.matrix([
      [X.get([0,0]) + dt*U.get([0,0])],
      [X.get([1,0]) + dt*beta*(X.get([2,0]) - X.get([1,0]))],
      [X.get([2,0]) - dt*alpha*X.get([0,0])]
    ])

    this.F = (X,U) => math.matrix([
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
    this.Q = math.matrix([
        [0.5,0,0],
        [0,1,0],
        [0,0,1]
    ])
    this.Q = math.square(this.Q)
    this.R = math.matrix([
        [2]
    ])
    this.R = math.square(this.R)

    this.U = math.matrix([[0]])
    this.Z = math.matrix([[this.initial_p]])
    this.intervals.push(
      setInterval(this.kalmanIteration, dt*1000)
    )
    this.intervals.push(
      setInterval(this.printX, 100)
    )
    if (this.playTone) {
      setTimeout(this.tonePlayer,1)
    }
    this.runningState = 2
  }



  kalmanIteration = () => {

    let Xkkm = this.f(this.X,this.U)
    let Pkkm = math.add(
      math.multiply(
        math.multiply(
          this.F(this.X,this.U),
          this.P
        ),
        math.transpose(this.F(this.X,this.U))
      ),
      this.Q
    )
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
  }

  printX = () => {
    this.setState({vz:this.X.get([0,0])})
    if (this.sendData) {
      data = {
        acc : this.acc,
        press : this.press
      }
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
  }

  tonePlayer = () => {
    let vz = this.X.get([0,0])
    let inter = 300 - 130*vz
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
          this.Z.subset(math.index(0,0), pressure*100)
        } else if (this.runningState == 0) {
          this.nb_init_p += 1
          this.initial_p += pressure*100
        }
      })
    )

    this.subscriptions.push(
      accelerometer.subscribe(({ x, y, z, timestamp }) => {
        if (this.runningState == 2) {
          this.acc = [x,y,z-this.g_const]
          this.U.subset(math.index(0,0), Math.sqrt(x*x+y*y+z*z)-this.g_const)
        } else if (this.runningState == 0) {
          this.nb_init_a += 1
          this.g_const += Math.sqrt(x*x+y*y+z*z)
          if (this.nb_init_a > 50 && this.nb_init_p > 50) {
            this.runningState = 1
            this.g_const /= this.nb_init_a
            this.initial_p /= this.nb_init_p
            this.initKalman()
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

  render = () => {
    return (
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
      </>
    )
  }

};


export default App;
