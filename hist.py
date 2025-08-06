import matplotlib.pyplot as plt
import h5py
import argparse
from . import regression

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('plot_which', type=str, choices=['GN2_minus_truth', 'reco_minus_truth', 'GN2', 'reco'])
parser.add_argument('xcoords', type=tuple)
parser.add_argument('ycoords', type=tuple)
parser.add_argument('--logarithmic', '-l', action='store_true')
parser.add_argument('--bins', '-b', type=int, default=100)
parser.add_argument('--skew', '-s', action='store_true')

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
plot_which = args.plot_which
xcoords = args.xcoords
ycoords = args.ycoords
islog = args.logarithmic
no_bins = args.bins
skew = args.skew

label_dict = {
    'GN2_minus_truth': 'GN2 Jet $p_T$ - Truth Jet $p_T$ / GeV',
    'reco_minus_truth': 'Reco Jet $p_T$ - Truth Jet $p_T$ / GeV',
    'GN2': 'GN2 Jet $p_T$ / GeV',
    'reco': 'Reco Jet $p_T$ / GeV'
}

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

plotx = jets['truth_pt']

if plot_which == 'GN2_minus_truth':
    ploty = jets['GN2_truth_pt'] - jets['truth_pt']
    if skew:
        m, c = regression.linear_regression(plotx, ploty)
        ploty = regression.skew_data(ploty, m, c)

elif plot_which == 'reco_minus_truth':
    ploty = jets['pt'] - jets['truth_pt']
    if skew:
        m, c = regression.linear_regression(plotx, ploty)
        ploty = regression.skew_data(ploty, m, c)

elif plot_which == 'GN2':
    ploty = jets['GN2_truth_pt']

elif plot_which == 'reco':
    ploty = jets['pt']


plt.figure(figsize=(12, 10))

if islog:
    plt.hist2d(plotx, ploty, bins=no_bins, range=[[xcoords[0], xcoords[1]], [ycoords[0], ycoords[1]]], cmap='jet', norm='log')
else:
    plt.hist2d(plotx, ploty, bins=no_bins, range=[[xcoords[0], xcoords[1]], [ycoords[0], ycoords[1]]], cmap='jet')

plt.ylabel(label_dict[plot_which])
plt.xlabel('Truth Jet $p_T$ / GeV')
plt.colorbar()

plt.savefig(output_file, bbox_inches='tight')
plt.close()