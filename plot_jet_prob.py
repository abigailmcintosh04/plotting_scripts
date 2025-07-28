import h5py 
from puma import Histogram, HistogramPlot
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('flavour', type=str)

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
flavour = args.flavour

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

light_mask = jets['flavour_label']