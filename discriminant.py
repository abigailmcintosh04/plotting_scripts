from ftag import Flavours
from ftag.utils import get_discriminant # type: ignore
import h5py
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)

args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

label_dict = {
    'b': '$b$-jets',
    'c': '$c$-jets'
}

discs_b = get_discriminant(
    jets=jets,
    tagger='GN2',
    signal=Flavours['bjets'],
    flavours=Flavours.by_category('single-btag'),
    fraction_values={'fc': 0.2, 'fu': 0.8, 'ftau': 0}
)

discs_c = get_discriminant(
jets=jets,
tagger='GN2',
signal=Flavours['cjets'],
flavours=Flavours.by_category('single-btag'),
fraction_values={'fb': 0.3, 'fu': 0.7, 'ftau': 0}
)

bins = np.linspace(-4, 4, 100)

plt.figure(figsize=(6.4, 4.8))

plt.hist(discs_b, bins=bins, color='tab:blue', histtype='step', linewidth=2, label=label_dict['b'], log=True, density=True)
plt.hist(discs_c, bins=bins, color='tab:green', histtype='step', linewidth=2, label=label_dict['c'], log=True, density=True)

plt.legend(loc='upper right')
plt.xlabel('Discriminant')
plt.ylabel('Normalised number of jets')
plt.margins(x=0)
plt.minorticks_on()
plt.tick_params(axis='both', which='both', direction='in', top=True, right=True)

plt.savefig(output_file, bbox_inches='tight', dpi=200)
plt.close()