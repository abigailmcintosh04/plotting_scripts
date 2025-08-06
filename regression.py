import scipy.stats as sc
# import matplotlib.pyplot as plt
# import argparse
# import h5py

def linear_regression(xdata, ydata):
    gradient, intercept, _, _, _ = sc.linregress(xdata, ydata)
    return gradient, intercept

def skew_data(ydata, gradient, intercept):
    ydata_new = (ydata - intercept) / (gradient + 1)
    return ydata_new


# parser = argparse.ArgumentParser()

# parser.add_argument('input_file', type=str)
# parser.add_argument('output_file', type=str)
# parser.add_argument('plot_which', type=str, choices=['GN2_minus_truth', 'reco_minus_truth', 'GN2', 'reco'])

# args = parser.parse_args()

# input_file = args.input_file
# output_file = args.output_file
# plot_which = args.plot_which

# label_dict = {
#     'GN2_minus_truth': 'GN2 Jet $p_T$ - Truth Jet $p_T$ / GeV',
#     'reco_minus_truth': 'Reco Jet $p_T$ - Truth Jet $p_T$ / GeV',
#     'GN2': 'GN2 Jet $p_T$ / GeV',
#     'reco': 'Reco Jet $p_T$ / GeV'
# }

# with h5py.File(input_file, 'r') as h5file:
#     jets = h5file['jets'][:]

# if plot_which == 'GN2_minus_truth':
#     ydata = jets['GN2_truth_pt'] - jets['truth_pt']
# elif plot_which == 'reco_minus_truth':
#     ydata = jets['pt'] - jets['truth_pt']
# elif plot_which == 'GN2':
#     ydata = jets['GN2_truth_pt']
# elif plot_which == 'reco':
#     ydata = jets['pt']

# xdata = jets['truth_pt']

# gradient, intercept, _, _, _ = sc.linregress(xdata, ydata)
# print(f'y = {gradient}x + {intercept}')


# plt.figure(figsize=(12, 10))
# plt.scatter(xdata, ydata, s=5)
# plt.axline(xy1=(0, intercept), slope=gradient, c='r')

# plt.xlim(0, 1000)
# plt.ylim(0, 1000)

# plt.ylabel(label_dict[plot_which])
# plt.xlabel('Truth Jet $p_T$ / GeV')

# plt.savefig(output_file, bbox_inches='tight')
# plt.close()