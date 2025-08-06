import h5py
import argparse
import regression # type: ignore

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('which', choices=['GN2', 'GN2_minus_truth'])
parser.add_argument('--custom_mc', '-c', nargs=2, type=float)

args = parser.parse_args()

input_file = args.input_file
output_file= args.output_file
custom_mc = args.custom_mc
which = args.which

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

xdata = jets['truth_pt']
if which == 'GN2_minus_truth':
    ydata = jets['GN2_truth_pt'] - jets['truth_pt']
elif which == 'GN2':
    ydata = jets['GN2_truth_pt']

if custom_mc is not None:
    m = custom_mc[0]
    c = custom_mc[1]
else:
    m, c = regression.linear_regression(xdata, ydata)  

updated_gn2_truth = regression.skew_data(xdata, ydata, m, c)
updated_gn2 = updated_gn2_truth + xdata

with h5py.File(output_file, 'w') as h5file:
    np_arr = jets[()]
    dset = h5file.create_dataset('jets', data=np_arr)
    dset['GN2_truth_pt'] = updated_gn2

