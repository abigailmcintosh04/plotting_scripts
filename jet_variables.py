import h5py
from puma import Histogram, HistogramPlot
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('parameter', type=str, choices=['truth_pt', 'pt', 'eta', 'phi', 'energy', 'mass', 'dr', 'GN2_truth_pt', 'jet_minus_truth', 'GN2_minus_truth'])

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
parameter = args.parameter

labels_dict = {
    'truth_pt': 'Jet Truth $p_T$ / GeV',
    'pt': 'Jet $p_T$ / GeV',
    'eta': 'Jet eta / rad',
    'phi': 'Jet phi / rad',
    'energy': 'Jet energy / GeV',
    'mass': 'Jet mass / GeV',
    'dr': '$Delta$R to nearest truth jet',
    'GN2_truth_pt': 'GN2 jet truth $p_T$ / GeV',
    'jet_minus_truth': 'Jet $p_T$ - truth jet $p_T$ / GeV',
    'GN2_minus_truth': 'GN2 $p_T$ - truth $p_T$ / GeV'
}

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

matched_mask = jets['is_matched'] == True
matched_jets = jets[matched_mask]

q_mask = matched_jets['flavour_label'] == 0
c_mask = matched_jets['flavour_label'] == 1
b_mask = matched_jets['flavour_label'] == 2

q_all = matched_jets[q_mask]
c_all = matched_jets[c_mask]
b_all = matched_jets[b_mask]

if parameter == 'jet_minus_truth':
    q_plot = q_all['pt'] - q_all['truth_pt']
    c_plot = c_all['pt'] - c_all['truth_pt']
    b_plot = b_all['pt'] - b_all['truth_pt']
elif parameter == 'GN2_minus_truth':
    q_plot = q_all['GN2_truth_pt'] - q_all['truth_pt']
    c_plot = c_all['GN2_truth_pt'] - c_all['truth_pt']
    b_plot = b_all['GN2_truth_pt'] - b_all['truth_pt']
else:
    q_plot = q_all[parameter]
    c_plot = c_all[parameter]
    b_plot = b_all[parameter]

h_q = Histogram(values=q_plot, flavour='ujets', bins=np.linspace(-1000, 1000, 100))
h_c = Histogram(values=c_plot, flavour='cjets', bins=np.linspace(-1000, 1000, 100))
h_b = Histogram(values=b_plot, flavour='bjets', bins=np.linspace(-1000, 1000, 100))


plot = HistogramPlot(
    ylabel='Normalised number of jets',
    xlabel=labels_dict[parameter],
    logy = True,
    atlas_brand = 'Muon Collider'
)

plot.add(h_q)
plot.add(h_c)
plot.add(h_b)

plot.draw()
plot.savefig(output_file)