# Copyright (c) 2015, Oleg Puzanov
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Demo for plotting RF propagation heatmap using the two-dimensional signal strength data
of 2.4 GHz Wi-Fi antenna.
The data is supplied in three CSV files: X coordinates, Y coordinates and Signal Strength in dBm.
The heatmap is drawn using Matplotlib and specific "adjustments" for transparency levels of
the color map to get a smooth gradient.
Initial implementation used the masked arrays and "pcolormesh" function, but switched to "contourf"
without the masked arrays, taking into account the issue with interpolation for masked arrays in Matplotlib.
At this stage the heatmap doesn't consider the penetration of obstacles, like walls,
and their impact on signal strength and propagation.
"""

from matplotlib import pyplot as plt
from matplotlib import image as im
import numpy as np

# Specific values for the antenna data and the floor plan
aspect = 2.7
num_levels = 512
min_signal_strength = -48
label_pos = -7
label_step = 8

# Reading CSV into numpy arrays
signal_strength_data = np.genfromtxt("data/Signal_Strength-Table.csv", delimiter=',')
x_data = np.genfromtxt("data/X-table.csv", delimiter=',')
y_data = np.genfromtxt("data/Y-table.csv", delimiter=',')

# Reading and adjusting the image dimensions according to the propagation heatmap
image = im.imread("data/floor_plan1.png")
image_w = image.shape[1]
image_h = image.shape[0]

plt.figure(figsize=(image_w/80, image_h/80), dpi=80)
wh_ratio = image_w/image_h

plt.imshow(image, origin='upper', extent=[x_data.min()*2*wh_ratio, x_data.max()*2*wh_ratio,
                                          y_data.min()*2, y_data.max()*2])

# Setting the transparency values for a smooth gradient
cmap = plt.get_cmap('Paired')
cmap._init()
cmap._lut[:, 3] = np.linspace(0.4, 0.8, len(cmap._lut[:, 3]))

# Plotting the filled contour heatmap
crf = plt.contourf(
    x_data*aspect, y_data*aspect, signal_strength_data,
    levels=np.linspace(min_signal_strength, signal_strength_data.max(), num_levels),
    cmap=cmap,
    ls='-',
    origin='upper',
    antialiased=True)

# Reading the tick labels generated for the color bar
cb = plt.colorbar()
labels = sorted([t.get_text() for t in cb.ax.get_yticklabels()])

# Drawing the labels along the contour levels
for l in labels:
    plt.text(label_pos, 0, l, fontsize=6)
    label_pos -= label_step
    label_step += 0.4

# Removing the color bar and plotting all figures
cb.remove()
plt.axis('off')
plt.show()
