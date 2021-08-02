# Variometer testing

## Various kalman models

See https://en.wikipedia.org/wiki/Kalman_filter and https://en.wikipedia.org/wiki/Extended_Kalman_filter

**Notations :**
- <img src="https://render.githubusercontent.com/render/math?math=\color{blue}X"> is the state of the system
- <img src="https://render.githubusercontent.com/render/math?math=\color{blue}U"> is the control vector
- <img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z"> is the observation

**Atmospheric model :**
- <img src="https://render.githubusercontent.com/render/math?math=\color{blue}m_%7Batmo%7D%28h%29+%3D+P_0+%5Cexp+%5Cleft%28+%5Cfrac%7B-Mgh%7D%7BRT_%7Bsea%7D%7D+%5Cright%29">
- <img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_0+%3D+101325+%5C+P_a">
- <img src="https://render.githubusercontent.com/render/math?math=\color{blue}M+%3D+0.02897+%5C+kg.mole%5E%7B-1%7D">
- <img src="https://render.githubusercontent.com/render/math?math=\color{blue}R+%3D+8.314+%5C+J.K%5E%7B-1%7D.mole%5E%7B-1%7D">


### V1 - No IMU
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bz%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5B%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bz%7D+%3D+0+%2B+u_1">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+m_%7Batmo%7D%28z%29+%2B+w_1">

### V2 - V1 with inertia modelling
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bz%2C+v_z%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5B%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bz%7D+%3D+v_z+%2B+u_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bv_z%7D+%3D+0+%2B+u_2">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+m_%7Batmo%7D%28z%29+%2B+w_1">

### V3 - V2 with IMU integrated in the inertia model
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bz%2C+v_z%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5Ba_%7Bz%2Cmes%7D%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bz%7D+%3D+v_z+%2B+u_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bv_z%7D+%3D+a_%7Bz%2Cmes%7D+%2B+u_2">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+m_%7Batmo%7D%28z%29+%2B+w_1">

### V4 - V2 with inertia modelling propagated to the vertical acceleration
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bz%2C+v_z%2C+a_z%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5B%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bz%7D+%3D+v_z+%2B+u_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bv_z%7D+%3D+a_z+%2B+u_2">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Ba_z%7D+%3D+0+%2B+u_2">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+m_%7Batmo%7D%28z%29+%2B+w_1">

### V5 - V4 with Imu as a sensor
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bz%2C+v_z%2C+a_z%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5B%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%2C+a_%7Bz%2Cmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bz%7D+%3D+v_z+%2B+u_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bv_z%7D+%3D+v_z+%2B+u_2">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Ba_z%7D+%3D+0+%2B+u_3">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+m_%7Batmo%7D%28z%29+%2B+w_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}a_%7Bz%2Cmes%7D+%3D+a_z+%2B+w_2">

### V6 - V5 with pressure shifting (as the Atmospheric model supposes a 101325 Pa pressure at sea level)
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bz%2C+v_z%2C+a_z%2C+P_1%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5B%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%2C+a_%7Bz%2Cmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bz%7D+%3D+v_z+%2B+u_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bv_z%7D+%3D+v_z+%2B+u_2">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Ba_z%7D+%3D+0+%2B+u_3">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7BP_1%7D+%3D+0+%2B+u_4">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+m_%7Batmo%7D%28z%29+%2B+P_1+%2B+w_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}a_%7Bz%2Cmes%7D+%3D+a_z+%2B+w_2">

### V7 - V5 with temperature shifting (as the Atmospheric model supposes a 288K temperature at sea level)
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bz%2C+v_z%2C+a_z%2C+T_%7Bsea%7D%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5B%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%2C+a_%7Bz%2Cmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bz%7D+%3D+v_z+%2B+u_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bv_z%7D+%3D+v_z+%2B+u_2">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Ba_z%7D+%3D+0+%2B+u_3">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7BT_%7Bsea%7D%7D+%3D+0+%2B+u_4">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+m_%7Batmo%7D%28z%2C+T_%7Bsea%7D%29+%2B+w_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}a_%7Bz%2Cmes%7D+%3D+a_z+%2B+w_2">

### V8 - V3 with a linear pressure model. It ignores the initial altitude.

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bv_z%2C+P%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5Ba_%7Bz%2Cmes%7D%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bv_z%7D+%3D+a_%7Bz%2Cmes%7D+%2B+u_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7BP%7D+%3D+-%5Calpha+v_z+%2B+u_2+%5Cquad+%5Calpha+%5Capprox+100%2F8">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+P+%2B+w_1">

### V9 - V8 with a model of the delay on pressure measurements

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}X+%3D+%5Bv_z%2C+P_%7Bint%7D%2C+P_%7Bext%7D%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}U+%3D+%5Ba_%7Bz%2Cmes%7D%5D">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}Z+%3D+%5BP_%7Bmes%7D%5D">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7Bv_z%7D+%3D+a_%7Bz%2Cmes%7D+%2B+u_1">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7BP_%7Bint%7D%7D+%3D+%5Cbeta+%28P_%7Bext%7D+-+P%7Bint%7D%29+%2B+u_2">
<img src="https://render.githubusercontent.com/render/math?math=\color{blue}%5Cdot%7BP_%7Bext%7D%7D+%3D+-%5Calpha+v_z+%2B+u_3+%5Cquad+%5Calpha+%5Capprox+100%2F8">

<img src="https://render.githubusercontent.com/render/math?math=\color{blue}P_%7Bmes%7D+%3D+P_%7Bint%7D+%2B+w_1">
