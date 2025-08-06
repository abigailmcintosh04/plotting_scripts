import scipy.stats as sc

def linear_regression(xdata, ydata):
    gradient, intercept, _, _, _ = sc.linregress(xdata, ydata)
    print(f'y = {gradient} * x + {intercept}')
    return gradient, intercept

def skew_data(xdata, ydata, gradient, intercept):
    line = gradient * xdata + intercept
    ydata_new = ydata - line
    return ydata_new
