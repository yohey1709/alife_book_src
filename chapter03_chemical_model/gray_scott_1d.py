#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# Simulation Parameters
VISUALIZATION_TIME = 128  # size of visualized time duration = visualization height
SPACE_SIZE = 256  # size of 1D space = visualization width
dx = 0.01
dt = 1
visualization_step = 4

# Model Parameters
Du = 2e-5
Dv = 1e-5
# amorphous
f, k = 0.04, 0.06
# spots
# f, k = 0.035, 0.065
# wandering bubbles
# f, k = 0.012, 0.05
# waves
# f, k = 0.025, 0.05

# Initialization
u = np.zeros((VISUALIZATION_TIME, SPACE_SIZE))
v = np.zeros((VISUALIZATION_TIME, SPACE_SIZE))
# set initiale square pattern on center
init_pattern_size = 20
u[0,:] = 1.0
v[0,:] = 0.0
u[0, SPACE_SIZE//2-init_pattern_size//2:SPACE_SIZE//2+init_pattern_size//2] = 0.5
v[0, SPACE_SIZE//2-init_pattern_size//2:SPACE_SIZE//2+init_pattern_size//2] = 0.25
# add random noize in order to break the square symmetry
u[0,:] += np.random.rand(SPACE_SIZE)*0.01
v[0,:] += np.random.rand(SPACE_SIZE)*0.01

# Animation setup
fig = plt.figure()
ax = plt.axes()
hmap = ax.imshow(u, vmin=0, vmax=1)
fig.colorbar(hmap)

def update(frame):
    global u, v
    for i in range(visualization_step):
        current_line = (frame * visualization_step + i) % VISUALIZATION_TIME
        next_line = (current_line + 1) % VISUALIZATION_TIME
        current_u = u[current_line]
        current_v = v[current_line]
        # calculate laplacian
        laplacian_u = (np.roll(current_u, 1) + np.roll(current_u, -1) - 2*current_u) / (dx*dx)
        laplacian_v = (np.roll(current_v, 1) + np.roll(current_v, -1) - 2*current_v) / (dx*dx)
        # Gray-Scott model equation
        dudt = Du*laplacian_u - current_u*current_v*current_v + f*(1.0-current_u)
        dvdt = Dv*laplacian_v + current_u*current_v*current_v - (f+k)*current_v
        u[next_line] = current_u + dt * dudt
        v[next_line] = current_v + dt * dvdt
    hmap.set_array(u)
    return hmap,

anim = animation.FuncAnimation(fig, update, interval=100, blit=True)
plt.show(anim)
