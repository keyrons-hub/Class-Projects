# Kieran Humphreys ECE 3250 Homework 7

import matplotlib.pyplot as plt
import numpy as np

# linear space for slip
x = np.linspace(0.001, 1, 1000)

# define circuit parameters
V1 = 254
Req = 3.4
Xeq = 19.5
Rc = 3280
R1 = 0.5
R2 = 2.9
Ws = 183.8
sl = (1 - x) / x

# define torque function as slip
I2 = V1 / (Req + Xeq + (R2 * sl))
T = (3 * (I2**2) * R2) / (x * Ws)

# define power developed as a function of slip
Pd = (3 * (V1**2) * (R2 * sl)) / (Req**2 + Xeq**2 + ((R2 * sl)**2) + (2 * Req * R2 * sl))

# define input power as a function of slip
Pin = (3 * V1**2) * ((((R2 * sl) + (R1 + R2)) / ( ((R1 + R2)**2) + Xeq**2 + ((R2 * sl)**2) + (2 * (R1 + R2) * R2 * sl))) + (1 / Rc))

# define efficiency as a function of slip
Eff = Pd / Pin

# create plots
fig = plt.figure()
plt.plot(x, T, 'g')
plt.xlim(max(x) + 0.1, min(x) - 0.1)
plt.plot(x, Pd, 'r')
plt.xlim(max(x) + 0.1, min(x) - 0.1)
plt.plot(x, Eff, 'b')
plt.xlim(max(x) + 0.1, min(x) - 0.1)
plt.show()
