import matplotlib.pyplot as plt
import argparse
import h5py
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('parameter1', type=str, choices=['reco', 'GN2'])
parser.add_argument('parameter2', type=str, choices=['reco', 'GN2'])
parser.add_argument('coords', nargs=2, type=float)

args = parser.parse_args()
input_file = args.input_file
parameter1 = args.parameter1
parameter2 = args.parameter2
coords = args.coords
output_file = args.output_file

labels_dict = {
    'reco': 'Jet $p_T$ - truth jet $p_T$ / GeV',
    'GN2': 'GN2 $p_T$ - truth $p_T$ / GeV',
}

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

valid_mask = jets['is_matched'] == True
valid = jets[valid_mask]

if parameter1 == 'reco':
    plot1 = valid['pt'] - valid['truth_pt']

elif parameter1 == 'GN2':
    plot1 = valid['GN2_truth_pt'] - valid['truth_pt']

if parameter2 == 'reco':
    plot2 = valid['pt'] - valid['truth_pt']

elif parameter2 == 'GN2':
    plot2 = valid['GN2_truth_pt'] - valid['truth_pt']

bins=np.linspace(coords[0], coords[1], 100)

plt.figure(figsize=(6.4, 4.8))

plt.hist(plot1, bins=bins, label=labels_dict[parameter1], color='b', log=True, histtype='step', linewidth=2)
plt.hist(plot2, bins=bins, label=labels_dict[parameter2], color='r', log=True, histtype='step', linewidth=2)
plt.legend(loc='lower left')
plt.ylabel('Normalised number of jets')
plt.margins(x=0)
plt.minorticks_on()
plt.tick_params(axis='both', which='both', direction='in', top=True, right=True)

# plt.tick_params(axis='x', which='minor', direction='in')

plt.savefig(output_file, bbox_inches='tight', dpi=200)
plt.close()
