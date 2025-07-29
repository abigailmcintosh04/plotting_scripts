import h5py
from puma import Histogram, HistogramPlot
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('parameter', type=str, choices=['d0', 'eta', 'phi', 'eta_rel', 'phi_rel', 'pt_frac', 'dr', 'z0', 'signed_2d_ip', 'signed_3d_ip'])

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
parameter = args.parameter

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

matched_jets_mask = jets['is_matched'] == True
matched_jets = jets[matched_jets_mask]
matched_tracks = consts[matched_jets_mask]

valid_track_mask = matched_tracks['valid'] == True
valid_tracks = matched_tracks[valid_track_mask]

q_mask = matched_jets['flavour_label'] == 0
c_mask = matched_jets['flavour_label'] == 1
b_mask = matched_jets['flavour_label'] == 2

q_all = matched_tracks[q_mask]
c_all = matched_tracks[c_mask]
b_all = matched_tracks[b_mask]
