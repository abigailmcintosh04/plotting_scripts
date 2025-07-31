import h5py
from puma import Histogram, HistogramPlot
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('parameter', type=str, choices=['d0', 'eta', 'phi', 'eta_rel', 'phi_rel', 'pt_frac', 'dr', 'z0', 'signed_2d_ip', 'signed_3d_ip'])
parser.add_argument('xmin', type=float)
parser.add_argument('xmax', type=float)

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
parameter = args.parameter
xmin = args.xmin
xmax = args.xmax

labels_dict = {
    'd0': 'Track $d_0$ / mm',
    'eta': 'Track $\eta$',
    'phi': 'Track $\phi$ / rad',
    'eta_rel': '$\Delta \eta$ between track and jet',
    'phi_rel': '$\Delta \phi$ between track and jet / rad',
    'pt_frac': 'Fractional $p_T$ of track',
    'dr': '$\Delta R$',
    'z0': '$z_0$ / mm',
    'signed_2d_ip': 'Signed 2D Impact Parameter Significance',
    'signed_3d_ip': 'Signed 3D Impact Parameter Significance'
}

with h5py.File(input_file, 'r') as h5file:
    consts = h5file['consts'][:]
    jets = h5file['jets'][:]

q_mask = jets['flavour_label'] == 0
c_mask = jets['flavour_label'] == 1
b_mask = jets['flavour_label'] == 2

q_all = consts[q_mask]
c_all = consts[c_mask]
b_all = consts[b_mask]

valid_q_mask = q_all['valid'] == True
valid_c_mask = c_all['valid'] == True
valid_b_mask = b_all['valid'] == True

q_tracks = q_all[valid_q_mask]
c_tracks = c_all[valid_c_mask]
b_tracks = b_all[valid_b_mask]

q_plot = q_tracks[parameter]
c_plot = c_tracks[parameter]
b_plot = b_tracks[parameter]

h_q = Histogram(values=q_plot, flavour='ujets', bins=np.linspace(xmin, xmax, 100))
h_c = Histogram(values=c_plot, flavour='cjets', bins=np.linspace(xmin, xmax, 100))
h_b = Histogram(values=b_plot, flavour='bjets', bins=np.linspace(xmin, xmax, 100))

plot = HistogramPlot(
    ylabel='Normalised number of jets',
    xlabel=labels_dict[parameter],
    logy=True,
    atlas_brand='Muon Collider'
)

plot.add(h_q)
plot.add(h_c)
plot.add(h_b)

plot.draw()
plot.savefig(output_file)