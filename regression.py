import numpy as np

def linear_regression(xdata, ydata):
    mc_arr = np.polyfit(xdata, ydata, 1)
    gradient = mc_arr[0]
    intercept = mc_arr[1]
    print(f'y = {gradient} * x + {intercept}')
    return gradient, intercept

def skew_data(xdata, ydata, gradient, intercept):
    line = gradient * xdata + intercept
    ydata_new = ydata - line
    return ydata_new
