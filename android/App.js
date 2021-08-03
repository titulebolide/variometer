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

const config = { }
const math = create(all, config)

const dt = 0.1
const beta = 1
const alpha = 100/8

setUpdateIntervalForType(SensorTypes.accelerometer, dt*1000);
setUpdateIntervalForType(SensorTypes.barometer, dt*1000);

class App extends React.Component {

  state = {vz:0}

  f = (X,U) => math.matrix([
    [X.get([0,0]) + dt*U.get([0,0])],
    [X.get([1,0]) + dt*beta*(X.get([2,0]) - X.get([1,0]))],
    [X.get([2,0]) - dt*alpha*X.get([0,0])]
  ])

  F = (X,U) => math.matrix([
    [1, 0, 0],
    [0, 1-dt*beta, dt*beta],
    [-dt*alpha, 0, 1]
  ])

  h = (X) => math.matrix([
    [X.get([1,0])]
  ])

  H = (X) => math.matrix([
    [0,1,0]
  ])

  X = math.matrix([
      [0],
      [84300],
      [84300]
  ])
  P = math.matrix([
      [0.2,0,0],
      [0,10,0],
      [0,0,10]
  ])
  P = math.square(this.P)
  Q = math.matrix([
      [0.2,0,0],
      [0,10,0],
      [0,0,10]
  ])
  Q = math.square(this.Q)
  R = math.matrix([
      [10]
  ])
  R = math.square(this.R)

  U = math.matrix([[0]])
  Z = math.matrix([[84300]])

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
  }

  componentDidMount = () => {
    this.subbaro = barometer.subscribe(({ pressure }) => {
      this.Z.subset(math.index(0,0), pressure*100)
    });

    this.subacc = accelerometer.subscribe(({ x, y, z, timestamp }) =>
      this.U.subset(math.index(0,0), z-10.15)
    );

    setInterval(this.kalmanIteration, dt*1000)
    setInterval(this.printX, 100)

  }

  render = () => {
    return (
      <>
      <Text>
        {this.state.vz}
      </Text>
      <Text>
        {this.U.get([0,0])}
      </Text>
      <Text>
        {this.Z.get([0,0])}
      </Text>
      <Text>
        {this.P.get([0,0])}
      </Text>
      </>
    )
  }

};


export default App;
