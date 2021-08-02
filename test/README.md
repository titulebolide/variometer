# Variometer testing

## Various kalman models

See https://en.wikipedia.org/wiki/Kalman_filter and https://en.wikipedia.org/wiki/Extended_Kalman_filter

**Notations :**
- $X$ is the state of the system
- $U$ is the control vector
- $Z$ is the observation

**Atmospheric model :**
- $m_{atmo}(h) = P_0 \exp \left( \frac{-Mgh}{RT_{sea}} \right)$
- $P_0 = 101325 \ P_a$
- $M = 0.02897 \ kg.mole^{-1}$
- $R = 8.314 \ J.K^{-1}.mole^{-1}$


### V1 - No IMU
$X = [z]$
$U = []$
$Z = [P_{mes}]$

$\dot{z} = 0 + u_1$

$P_{mes} = m_{atmo}(z) + w_1$

### V2 - V1 with inertia modelling
$X = [z, v_z]$
$U = []$
$Z = [P_{mes}]$

$\dot{z} = v_z + u_1$
$\dot{v_z} = 0 + u_2$

$P_{mes} = m_{atmo}(z) + w_1$

### V3 - V2 with IMU integrated in the inertia model
$X = [z, v_z]$
$U = [a_{z,mes}]$
$Z = [P_{mes}]$

$\dot{z} = v_z + u_1$
$\dot{v_z} = a_{z,mes} + u_2$

$P_{mes} = m_{atmo}(z) + w_1$

### V4 - V2 with inertia modelling propagated to the vertical acceleration
$X = [z, v_z, a_z]$
$U = []$
$Z = [P_{mes}]$

$\dot{z} = v_z + u_1$
$\dot{v_z} = a_z + u_2$
$\dot{a_z} = 0 + u_2$

$P_{mes} = m_{atmo}(z) + w_1$

### V5 - V4 with Imu as a sensor
$X = [z, v_z, a_z]$
$U = []$
$Z = [P_{mes}, a_{z,mes}]$

$\dot{z} = v_z + u_1$
$\dot{v_z} = v_z + u_2$
$\dot{a_z} = 0 + u_3$

$P_{mes} = m_{atmo}(z) + w_1$
$a_{z,mes} = a_z + w_2$

### V6 - V5 with pressure shifting (as the Atmospheric model supposes a 101325 Pa pressure at sea level)
$X = [z, v_z, a_z, P_1]$
$U = []$
$Z = [P_{mes}, a_{z,mes}]$

$\dot{z} = v_z + u_1$
$\dot{v_z} = v_z + u_2$
$\dot{a_z} = 0 + u_3$
$\dot{P_1} = 0 + u_4$

$P_{mes} = m_{atmo}(z) + P_1 + w_1$
$a_{z,mes} = a_z + w_2$

### V7 - V5 with temperature shifting (as the Atmospheric model supposes a 288K temperature at sea level)
$X = [z, v_z, a_z, T_{sea}]$
$U = []$
$Z = [P_{mes}, a_{z,mes}]$

$\dot{z} = v_z + u_1$
$\dot{v_z} = v_z + u_2$
$\dot{a_z} = 0 + u_3$
$\dot{T_{sea}} = 0 + u_4$

$P_{mes} = m_{atmo}(z, T_{sea}) + w_1$
$a_{z,mes} = a_z + w_2$

### V8 - V3 with a linear pressure model. It ignores the initial altitude.

$X = [v_z, P_{ext}]$
$U = [a_{z,mes}]$
$Z = [P_{mes}]$

$\dot{v_z} = a_{z,mes} + u_1$
$\dot{P_{ext}} = -\alpha v_z + u_2 \quad \alpha \approx 100/8$

$P_{mes} = P_{ext} + w_1$

### V9 - V8 with a model of the delay on pressure measurements

$X = [v_z, P_{int}, P_{ext}]$
$U = [a_{z,mes}]$
$Z = [P_{mes}]$

$\dot{v_z} = a_{z,mes} + u_1$
$\dot{P_{int}} = \beta (P_{ext} - P{int}) + u_2$
$\dot{P_{ext}} = -\alpha v_z + u_3 \quad \alpha \approx 100/8$

$P_{mes} = P_{int} + w_1$
