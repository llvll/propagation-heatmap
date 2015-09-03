# RF Propagation Heatmap
### *Demo for plotting RF propagation heatmap using the two-dimensional signal strength data of 2.4 GHz Wi-Fi antenna.*

![Screenshot](/ip[y]/rf_heatmap.png)

The data is supplied in three CSV files: X coordinates, Y coordinates and Signal Strength in dBm.

The heatmap is drawn using Matplotlib and specific "adjustments" for transparency levels of
the color map to get a smooth gradient.

Initial implementation used the masked arrays and "pcolormesh" function, but switched to "contourf" without the masked arrays, taking into account the issue with interpolation for masked arrays in Matplotlib.

At this stage the heatmap doesn't consider the penetration of obstacles, like walls,
and their impact on signal strength and propagation.

IPython Notebook (.ipynb file) is included for step-by-step execution of the demo application with extra comments.
