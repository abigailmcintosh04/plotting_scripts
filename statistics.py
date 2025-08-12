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

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]
    consts = h5file['consts'][:]

valid_mask = consts['valid'] == True
valid_consts = consts[valid_mask]

if jetortrack == 'jet':
    dataset = jets[parameter]

elif jetortrack == 'consts':
    dataset = valid_consts[parameter]

mean = np.mean(dataset)
std = np.std(dataset)

print(f'{parameter}\nMean: {mean}\nStandard Deviation: {std}')
