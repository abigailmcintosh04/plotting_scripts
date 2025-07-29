import h5py
from puma import Histogram, HistogramPlot
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('parameter', type=str, choices=['truth_pt', 'pt', 'eta', 'phi', 'energy', 'mass', 'dr'])

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
    'dr': '$Delta$R to nearest truth jet'
}

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

matched_mask = jets['is_matched'] == True
matched_jets = jets[matched_mask]

q_mask = matched_jets['flavour_label'] == 0
c_mask = matched_jets['flavour_label'] == 1
b_mask = matched_jets['flavour_label'] == 2

q_plot = matched_jets[q_mask]
c_plot = matched_jets[c_mask]
b_plot = matched_jets[b_mask]

h_q = Histogram(values=q_plot[parameter], flavour='ujets', bins=100)
h_c = Histogram(values=c_plot[parameter], flavour='cjets', bins=100)
h_b = Histogram(values=b_plot[parameter], flavour='bjets', bins=100)


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