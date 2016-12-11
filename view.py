# display a network's first layer weights
# as line chart or sound wav

import sys
if(len(sys.argv) > 1):
  filename = sys.argv[1]
else: filename = "trained.pkl"
print "loading network file", filename


from nntester import NnTester
nnTester = NnTester(filename)
data = nnTester.getLayerData()

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

# data = np.zeros((length))
fig, ax = plt.subplots()
ax.plot(data)
ax.axis((0, len(data), -10, 10))
ax.set_yticks([0])
ax.yaxis.grid(True)
# ax.tick_params(bottom='off', top='off', labelbottom='off',
           # right='off', left='off', labelleft='off')
fig.tight_layout(pad=0)
plt.show()
