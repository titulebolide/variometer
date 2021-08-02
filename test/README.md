# Variometer testing

## Various kalman models

See https://en.wikipedia.org/wiki/Kalman_filter and https://en.wikipedia.org/wiki/Extended_Kalman_filter

**Notations :**
- <img src="https://render.githubusercontent.com/render/math?math=X" style="background:white;padding:4px;"> is the state of the system
- <img src="https://render.githubusercontent.com/render/math?math=U" style="background:white;padding:4px;"> is the control vector
- <img src="https://render.githubusercontent.com/render/math?math=Z" style="background:white;padding:4px;"> is the observation

**Atmospheric model :**
- <img src="https://render.githubusercontent.com/render/math?math=m_{atmo}(h) = P_0 \exp \left( \frac{-Mgh}{RT_{sea}} \right)" style="background:white;padding:4px;">
- <img src="https://render.githubusercontent.com/render/math?math=P_0 = 101325 \ P_a" style="background:white;padding:4px;">
- <img src="https://render.githubusercontent.com/render/math?math=M = 0.02897 \ kg.mole^{-1}" style="background:white;padding:4px;">
- <img src="https://render.githubusercontent.com/render/math?math=R = 8.314 \ J.K^{-1}.mole^{-1}" style="background:white;padding:4px;">


### V1 - No IMU
<img src="https://render.githubusercontent.com/render/math?math=X = [z]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = []" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{z} = 0 + u_1" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = m_{atmo}(z) + w_1" style="background:white;padding:4px;">

### V2 - V1 with inertia modelling
<img src="https://render.githubusercontent.com/render/math?math=X = [z, v_z]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = []" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{z} = v_z + u_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{v_z} = 0 + u_2" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = m_{atmo}(z) + w_1" style="background:white;padding:4px;">

### V3 - V2 with IMU integrated in the inertia model
<img src="https://render.githubusercontent.com/render/math?math=X = [z, v_z]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = [a_{z,mes}]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{z} = v_z + u_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{v_z} = a_{z,mes} + u_2" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = m_{atmo}(z) + w_1" style="background:white;padding:4px;">

### V4 - V2 with inertia modelling propagated to the vertical acceleration
<img src="https://render.githubusercontent.com/render/math?math=X = [z, v_z, a_z]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = []" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{z} = v_z + u_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{v_z} = a_z + u_2" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{a_z} = 0 + u_2" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = m_{atmo}(z) + w_1" style="background:white;padding:4px;">

### V5 - V4 with Imu as a sensor
<img src="https://render.githubusercontent.com/render/math?math=X = [z, v_z, a_z]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = []" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}, a_{z,mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{z} = v_z + u_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{v_z} = v_z + u_2" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{a_z} = 0 + u_3" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = m_{atmo}(z) + w_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=a_{z,mes} = a_z + w_2" style="background:white;padding:4px;">

### V6 - V5 with pressure shifting (as the Atmospheric model supposes a 101325 Pa pressure at sea level)
<img src="https://render.githubusercontent.com/render/math?math=X = [z, v_z, a_z, P_1]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = []" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}, a_{z,mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{z} = v_z + u_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{v_z} = v_z + u_2" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{a_z} = 0 + u_3" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{P_1} = 0 + u_4" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = m_{atmo}(z) + P_1 + w_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=a_{z,mes} = a_z + w_2" style="background:white;padding:4px;">

### V7 - V5 with temperature shifting (as the Atmospheric model supposes a 288K temperature at sea level)
<img src="https://render.githubusercontent.com/render/math?math=X = [z, v_z, a_z, T_{sea}]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = []" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}, a_{z,mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{z} = v_z + u_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{v_z} = v_z + u_2" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{a_z} = 0 + u_3" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{T_{sea}} = 0 + u_4" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = m_{atmo}(z, T_{sea}) + w_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=a_{z,mes} = a_z + w_2" style="background:white;padding:4px;">

### V8 - V3 with a linear pressure model. It ignores the initial altitude.

<img src="https://render.githubusercontent.com/render/math?math=X = [v_z, P]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = [a_{z,mes}]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{v_z} = a_{z,mes} + u_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{P} = -\alpha v_z + u_2 \quad \alpha \approx 100/8" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = P + w_1" style="background:white;padding:4px;">

### V9 - V8 with a model of the delay on pressure measurements

<img src="https://render.githubusercontent.com/render/math?math=X = [v_z, P_{int}, P_{ext}]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=U = [a_{z,mes}]" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=Z = [P_{mes}]" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=\dot{v_z} = a_{z,mes} + u_1" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{P_{int}} = \beta (P_{ext} - P{int}) + u_2" style="background:white;padding:4px;">
<img src="https://render.githubusercontent.com/render/math?math=\dot{P_{ext}} = -\alpha v_z + u_3 \quad \alpha \approx 100/8" style="background:white;padding:4px;">

<img src="https://render.githubusercontent.com/render/math?math=P_{mes} = P_{int} + w_1" style="background:white;padding:4px;">
