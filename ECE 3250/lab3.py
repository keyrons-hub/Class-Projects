import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Kieran Humphreys kdh8az ECE 3251 Lab 3

fig = plt.figure(figsize = (4, 4))
ax = fig.add_subplot(111, projection = '3d')

ax.scatter(0, 0, 0.32)
ax.scatter(0, 0.1, 0.66)

plt.show()