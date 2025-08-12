import argparse
import h5py

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)

args = parser.parse_args()
input_file = args.input_file

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

tot = len(matched_jets)
tot_3 = tot / 3

q_weight = len(q_plot) / tot_3
c_weight = len(c_plot) / tot_3
b_weight = len(b_plot) / tot_3

print(f'Weights\nq: {q_weight}\nc: {c_weight}\nb: {b_weight}')