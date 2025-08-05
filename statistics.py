import numpy as np
import argparse
import h5py

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('parameter', type=str,choices=['truth_pt', 'pt', 'eta', 'phi', 'energy', 'mass', 'dr', 
                                                    'GN2_truth_pt', 'jet_minus_truth', 'GN2_minus_truth', 'GN2_truth_rel'])
parser.add_argument('mean_or_median', type=str, choices=['mean', 'median'])

args = parser.parse_args()
input_file = args.input_file
parameter = args.parameter
mean_or_median = args.mean_or_median

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

if parameter == 'jet_minus_truth':
    dataset = jets['pt'] - jets['truth_pt']

elif parameter == 'GN2_minus_truth':
    dataset = jets['GN2_truth_pt'] - jets['truth_pt']

elif parameter == 'GN2_truth_rel':
    dataset = (jets['GN2_truth_pt'] - jets['truth_pt']) / jets['truth_pt']

else:
    dataset = jets[parameter]

if mean_or_median == 'mean':
    oper = np.mean(dataset)
elif mean_or_median == 'median':
    oper = np.median(dataset)

std = np.std(dataset)

print(f'{mean_or_median.capitalize()}: {oper}\nStandard Deviation: {std}')
