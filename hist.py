import matplotlib.pyplot as plt
import h5py
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('plot_which', type=str, choices=['GN2_minus_truth', 'reco_minus_truth', 'GN2', 'reco'])
parser.add_argument('xmin', type=float)
parser.add_argument('xmax', type=float)
parser.add_argument('ymin', type=float)
parser.add_argument('ymax', type=float)
parser.add_argument('--logarithmic', '-l', action='store_true')
parser.add_argument('--bins', '-b', type=int, default=100)

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
plot_which = args.plot_which
xmin = args.xmin
xmax = args.xmax
ymin = args.ymin
ymax = args.ymax
islog = args.logarithmic
no_bins = args.bins

label_dict = {
    'GN2_minus_truth': 'GN2 Jet $p_T$ - Truth Jet $p_T$ / GeV',
    'reco_minus_truth': 'Reco Jet $p_T$ - Truth Jet $p_T$ / GeV',
    'GN2': 'GN2 Jet $p_T$ / GeV',
    'reco': 'Reco Jet $p_T$ / GeV'
}

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

truth_pt = jets['truth_pt']
# opt_pt = []

if plot_which == 'GN2_minus_truth':
    opt = jets['GN2_truth_pt'] - jets['truth_pt']
elif plot_which == 'reco_minus_truth':
    opt = jets['pt'] - jets['truth_pt']
elif plot_which == 'GN2':
    opt = jets['GN2_truth_pt']
elif plot_which == 'reco':
    opt = jets['pt']

plt.figure(figsize=(12, 10))

if islog:
    plt.hist2d(truth_pt, opt, bins=no_bins, range=[[xmin, xmax], [ymin, ymax]], cmap='jet', norm='log')
else:
    plt.hist2d(truth_pt, opt, bins=no_bins, range=[[xmin, xmax], [ymin, ymax]], cmap='jet')

plt.ylabel(label_dict[plot_which])
plt.xlabel('Truth Jet $p_T$ / GeV')
plt.colorbar()

plt.savefig(output_file, bbox_inches='tight')
plt.close()