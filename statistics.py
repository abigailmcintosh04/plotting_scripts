import numpy as np
import argparse
import h5py

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('jetortrack', type=str, choices=['jet', 'consts'])
parser.add_argument('parameter', type=str)

args = parser.parse_args()
input_file = args.input_file
jetortrack = args.jetortrack
parameter = args.parameter

if jetortrack == 'consts':
    with h5py.File(input_file, 'r') as h5file:
        data = h5file['consts'][:] 
    valid_mask = data['valid'] == True
    data = data[valid_mask]
    dataset = data[parameter]

elif jetortrack == 'jet':
    with h5py.File(input_file, 'r') as h5file:
        jets = h5file['jets'][:]
    if parameter == 'GN2_minus_truth':
        dataset = jets['GN2_truth_pt'] - jets['truth_pt']
    elif parameter == 'jet_minus_truth':
        dataset = jets['pt'] - jets['truth_pt']
    else:
        dataset = jets[parameter]

mean = np.mean(dataset)
std = np.std(dataset)

print(f'{parameter}\nMean: {mean}\nStandard Deviation: {std}')
