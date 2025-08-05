import matplotlib.pyplot as plt
import h5py
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('plot_which', type=str, choices=['GN2', 'reco'])
parser.add_argument('xmin', type=float)
parser.add_argument('xmax', type=float)
parser.add_argument('ymin', type=float)
parser.add_argument('ymax', type=float)

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
plot_which = args.plot_which
xmin = args.xmin
xmax = args.xmax
ymin = args.ymin
ymax = args.ymax

label_dict = {
    'GN2': 'GN2 Jet $p_T$ - Truth Jet $p_T$',
    'reco': 'Jet $p_T$ - Truth Jet $p_T$'
}

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

truth_pt = jets['truth_pt']
# opt_pt = []

if plot_which == 'GN2':
    opt_pt = jets['GN2_truth_pt']
elif plot_which == 'reco':
    opt_pt = jets['pt']

opt_minus_truth = opt_pt - truth_pt

plt.figure(figsize=(10, 10))

plt.hist2d(truth_pt, opt_minus_truth, bins=100, range=[[xmin, xmax], [ymin, ymax]], cmap='inferno')
plt.ylabel(label_dict[plot_which])
plt.xlabel('Truth Jet $p_T$')

plt.savefig(output_file, bbox_inches='tight')
plt.close()