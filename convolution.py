import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal

# Define signals
def sig_square(x):
    return 0 if x < 3 or x > 5 else 2

def sig_triag(x):
    return 0 if x < 0 or x > 2 else x

# Generate signals
sig1 = np.array([sig_square(x / 100) for x in range(1000)])  # Square pulse
sig2 = np.array([sig_triag(x / 100) for x in range(200)])     # Triangle pulse

# Prepare convolution computation
c = signal.convolve(sig1, sig2)  # Full convolution
c_length = len(c)

# Setup the figure
fig, axes = plt.subplots(3, 1, figsize=(8, 8))

ax1, ax2, ax3 = axes  # Assigning subplots

ax1.set_title("Signal 1 (Square Pulse)")
ax1.set_xlim(0, len(sig1))
ax1.set_ylim(0, max(sig1) + 1)
line1, = ax1.plot([], [], 'b', lw=2)

ax2.set_title("Signal 2 (Triangle Pulse)")
ax2.set_xlim(0, len(sig2))
ax2.set_ylim(0, max(sig2) + 1)
line2, = ax2.plot([], [], 'r', lw=2)

ax3.set_title("Convolution")
ax3.set_xlim(0, c_length)
ax3.set_ylim(0, max(c) + 1)
line3, = ax3.plot([], [], 'g', lw=2)

# Initialization function
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line1, line2, line3

# Update function
def update(frame):
    # Update the first two signals
    line1.set_data(np.arange(len(sig1[:frame])), sig1[:frame])
    line2.set_data(np.arange(len(sig2[:frame])), sig2[:frame])

    # Update convolution result dynamically
    line3.set_data(np.arange(frame), c[:frame])

    return line1, line2, line3

# Create animation
ani = animation.FuncAnimation(fig, update, frames=c_length, init_func=init, blit=True, interval=1)

plt.tight_layout()
plt.show()
