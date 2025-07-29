import h5py 
from puma import Histogram, HistogramPlot
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('flavour', type=str, choices=['u', 'c', 'b'])

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
flav = args.flavour

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

selected_flavour = f'GN2_p{flav}'

h_q = Histogram(values=q_plot[selected_flavour], flavour='ujets', bins=100, bins_range=(0,1))
h_c = Histogram(values=c_plot[selected_flavour], flavour='cjets', bins=100, bins_range=(0,1))
h_b = Histogram(values=b_plot[selected_flavour], flavour='bjets', bins=100, bins_range=(0,1))

plot = HistogramPlot(
    ylabel='Normalised number of jets',
    xlabel=f'${flav}$-jets probability',
    logy = True,
    atlas_brand = 'Muon Collider'
)

plot.add(h_q)
plot.add(h_c)
plot.add(h_b)

plot.draw()
plot.savefig(output_file)
