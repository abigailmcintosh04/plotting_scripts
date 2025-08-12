import argparse
import h5py
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('range', nargs=2, type=float)

args = parser.parse_args()

input_file = args.input_file
range = args.range
output_file = args.output_file

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

lower_mask = jets['GN2_truth_pt'] >= range[0]
upper_mask = jets['GN2_truth_pt'] <= range[1]

in_range_mask = np.logical_and(lower_mask, upper_mask)
out_range_mask = np.logical_not(in_range_mask)

in_range = jets[in_range_mask]
out_range = jets[out_range_mask]

with h5py.File(f'{output_file[:-3]}_inrange.h5', 'w') as h5file:
    np_arr = in_range[()]
    dset = h5file.create_dataset('jets', data=np_arr)

with h5py.File(f'{output_file[:-3]}_outrange.h5', 'w') as h5file:
    np_arr = out_range[()]
    dset = h5file.create_dataset('jets', data=np_arr)
