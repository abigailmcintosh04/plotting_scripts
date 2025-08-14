import matplotlib.pyplot as plt
import argparse
import h5py
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('parameter1', type=str, choices=['jet_minus_truth', 'GN2_minus_truth', 'pt', 'truth_pt', 'GN2_truth_pt'])
parser.add_argument('parameter2', type=str, choices=['jet_minus_truth', 'GN2_minus_truth', 'pt', 'truth_pt', 'GN2_truth_pt'])
parser.add_argument('--parameter3', '-p', type=str, choices=['jet_minus_truth', 'GN2_minus_truth', 'pt', 'truth_pt', 'GN2_truth_pt'])
parser.add_argument('coords', nargs=2, type=float)
parser.add_argument('--range', '-r', nargs=2, type=float)
parser.add_argument('--bins', '-b', default=100, type=int)
parser.add_argument('--normalised', '-n', action='store_true')

args = parser.parse_args()
input_file = args.input_file
parameter1 = args.parameter1
parameter2 = args.parameter2
parameter3 = args.parameter3
coords = args.coords
output_file = args.output_file
range = args.range
no_bins = args.bins
normalised = args.normalised

xlabels = {
    'truth_pt': '$p_T$ / GeV',
    'pt': '$p_T$ / GeV',
    'GN2_truth_pt': '$p_T$ / GeV',
    'jet_minus_truth': 'Predicted $p_T$ - Truth $p_T$ / GeV',
    'GN2_minus_truth': 'Predicted $p_T$ - Truth $p_T$ / GeV',
}

upper_labels = {
    'truth_pt': 'Truth $p_T$',
    'pt': 'Reco $p_T$',
    'GN2_truth_pt': 'GN2 $p_T$',
    'jet_minus_truth': 'Reco $p_T$',
    'GN2_minus_truth': 'GN2 $p_T$',
}

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

valid_mask = jets['is_matched'] == True
valid = jets[valid_mask]

if range is not None:
    pt_lower = valid['pt'] >= range[0]
    pt_upper = valid['pt'] <= range[1]
    pt_mask = np.logical_and(pt_lower, pt_upper)
    filtered_pt = valid['pt'][pt_mask]

    truth_lower = valid['truth_pt'] >= range[0]
    truth_upper = valid['truth_pt'] <= range[1]
    truth_mask = np.logical_and(truth_lower, truth_upper)
    filtered_truth = valid['truth_pt'][truth_mask]

    gn2_lower = valid['GN2_truth_pt'] >= range[0]
    gn2_upper = valid['GN2_truth_pt'] <= range[1]
    gn2_mask = np.logical_and(gn2_lower, gn2_upper)
    filtered_gn2 = valid['GN2_truth_pt'][gn2_mask]

else:
    filtered_pt = jets['pt']
    filtered_truth = jets['truth_pt']
    filtered_gn2 = jets['GN2_truth_pt']

if parameter1 == 'jet_minus_truth':
    plot1 = filtered_pt - filtered_truth
elif parameter1 == 'GN2_minus_truth':
    plot1 = filtered_gn2 - filtered_truth
elif parameter1 == 'pt':
    plot1 = filtered_pt
elif parameter1 == 'truth_pt':
    plot1 = filtered_truth
elif parameter1 == 'GN2_truth_pt':
    plot1 = filtered_gn2

if parameter2 == 'jet_minus_truth':
    plot2 = valid['pt'] - valid['truth_pt']
elif parameter2 == 'GN2_minus_truth':
    plot2 = valid['GN2_truth_pt'] - valid['truth_pt']
elif parameter2 == 'pt':
    plot2 = filtered_pt
elif parameter2 == 'truth_pt':
    plot2 = filtered_truth
elif parameter2 == 'GN2_truth_pt':
    plot2 = filtered_gn2

if parameter3 is not None:
    if parameter3 == 'jet_minus_truth':
        plot3 = valid['pt'] - valid['truth_pt']
    elif parameter3 == 'GN2_minus_truth':
        plot3 = valid['GN2_truth_pt'] - valid['truth_pt']
    elif parameter3 == 'pt':
        plot3 = filtered_pt
    elif parameter3 == 'truth_pt':
        plot3 = filtered_truth
    elif parameter3 == 'GN2_truth_pt':
        plot3 = filtered_gn2

bins=np.linspace(coords[0], coords[1], no_bins)

plt.figure(figsize=(6.4, 4.8))

if normalised:
    plt.hist(plot1, bins=bins, label=upper_labels[parameter1], color='b', log=True, histtype='step', linewidth=2, density=True)
    plt.hist(plot2, bins=bins, label=upper_labels[parameter2], color='r', log=True, histtype='step', linewidth=2, density=True)
    if parameter3 is not None:
        plt.hist(plot3, bins=bins, label=upper_labels[parameter3], color='g', log=True, histtype='step', linewidth=2, density=True)
    plt.ylabel('Normalised number of jets')
else:
    plt.hist(plot1, bins=bins, label=upper_labels[parameter1], color='b', log=True, histtype='step', linewidth=2)
    plt.hist(plot2, bins=bins, label=upper_labels[parameter2], color='r', log=True, histtype='step', linewidth=2)
    if parameter3 is not None:
        plt.hist(plot3, bins=bins, label=upper_labels[parameter3], color='g', log=True, histtype='step', linewidth=2)
    plt.ylabel('Number of jets')

plt.legend(loc='upper right')
plt.xlabel(xlabels[parameter1])
plt.margins(x=0)
plt.minorticks_on()
plt.tick_params(axis='both', which='both', direction='in', top=True, right=True)

# plt.tick_params(axis='x', which='minor', direction='in')

plt.savefig(output_file, bbox_inches='tight', dpi=200)
plt.close()
