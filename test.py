import numpy as np 


def hann_window_new(x_list, y_list, t_width):
    #### Determine how many segements will be used
    x = np.array(x_list)
    y = np.array(y_list) 
    half_width = t_width / 2.0
    weighted_mean_list = [] 
    for t0 in x:        
        indices = np.where((x >= t0 - half_width) & (x <= t0 + half_width))[0]
        x_window = x[indices]
        y_window = y[indices]
        relative_positions = (x_window - (t0 - half_width)) / t_width
        hann_weights = 0.5 * (1 - np.cos(2 * np.pi * relative_positions))
        weighted_mean = np.sum(hann_weights * y_window) / np.sum(hann_weights)
        weighted_mean_list.append(weighted_mean)
    return weighted_mean


x = np.arange(1850, 2101, 1)
y = np.random.rand(251)
t_width = 33.6295
hann_window_new(x, y, t_width)