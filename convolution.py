import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def sig_square(x):
  return 0 if x < 3 or x > 5 else 2

def sig_triag(x):
  return 0 if x < 0 or x > 2 else x

# First signal (square pulse)
sig1 = [sig_square(x/100) for x in range(1000)]

# Seconds signal (triangle pulse)
sig2 = [sig_triag(x/100) for x in range(200)]

c = signal.convolve(sig1,sig2)

plt.plot(np.abs(c))
plt.show()
