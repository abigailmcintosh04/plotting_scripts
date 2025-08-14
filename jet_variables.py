import h5py
from puma import Histogram, HistogramPlot
import matplotlib.pyplot as plt
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('parameter', type=str, choices=['truth_pt', 'pt', 'eta', 'phi', 'energy', 'mass', 'dr', 
                                                    'GN2_truth_pt', 'jet_minus_truth', 'GN2_minus_truth', 'GN2_truth_rel'])
parser.add_argument('xmin', type=float)
parser.add_argument('xmax', type=float)
parser.add_argument('--regression_only', '-r', action='store_true')

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
parameter = args.parameter
xmin = args.xmin
xmax = args.xmax
regression_only = args.regression_only

labels_dict = {
    'truth_pt': 'Jet Truth $p_T$ / GeV',
    'pt': 'Jet $p_T$ / GeV',
    'eta': 'Jet eta / rad',
    'phi': 'Jet phi / rad',
    'energy': 'Jet energy / GeV',
    'mass': 'Jet mass / GeV',
    'dr': '$\Delta$R to nearest truth jet',
    'GN2_truth_pt': 'GN2 jet truth $p_T$ / GeV',
    'jet_minus_truth': 'Jet $p_T$ - truth jet $p_T$ / GeV',
    'GN2_minus_truth': 'GN2 $p_T$ - truth $p_T$ / GeV',
    'GN2_truth_rel': '(GN2 $p_T$ - truth $p_T$) / truth $p_T$'
}

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

matched_mask = jets['is_matched'] == True
matched_jets = jets[matched_mask]

# if only regression, don't split into flavours.
if regression_only:

    if parameter == 'jet_minus_truth':
        all_plot = matched_jets['pt'] - matched_jets['truth_pt']

    elif parameter == 'GN2_minus_truth':
        all_plot = matched_jets['GN2_truth_pt'] - matched_jets['truth_pt']

    elif parameter == 'GN2_truth_rel':
        all_plot = (matched_jets['GN2_truth_pt'] - matched_jets['truth_pt']) / matched_jets['truth_pt']
        
    else:
        all_plot = matched_jets[parameter]

    bins=np.linspace(xmin, xmax, 100)

    plt.figure(figsize=(6.4, 4.8))

    plt.hist(all_plot, bins=bins, label=labels_dict[parameter], color='tab:blue', log=True, histtype='step', linewidth=2, density=True)
    plt.legend(loc='upper right')
    plt.ylabel('Normalised number of jets')
    plt.margins(x=0)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True)

    plt.savefig(output_file, bbox_inches='tight', dpi=200)
    plt.close()


else:

    plot = HistogramPlot(ylabel='Normalised number of jets', 
                         xlabel=labels_dict[parameter],
                        logy = True,
                        atlas_brand = 'Muon Collider')

    q_mask = matched_jets['flavour_label'] == 0
    c_mask = matched_jets['flavour_label'] == 1
    b_mask = matched_jets['flavour_label'] == 2

    q_all = matched_jets[q_mask]
    c_all = matched_jets[c_mask]
    b_all = matched_jets[b_mask]

    if parameter == 'jet_minus_truth':
        q_plot = q_all['pt'] - q_all['truth_pt']
        c_plot = c_all['pt'] - c_all['truth_pt']
        b_plot = b_all['pt'] - b_all['truth_pt']

    elif parameter == 'GN2_minus_truth':
        q_plot = q_all['GN2_truth_pt'] - q_all['truth_pt']
        c_plot = c_all['GN2_truth_pt'] - c_all['truth_pt']
        b_plot = b_all['GN2_truth_pt'] - b_all['truth_pt']
        
    elif parameter == 'GN2_truth_rel':
        q_plot = (q_all['GN2_truth_pt'] - q_all['truth_pt']) / q_all['truth_pt']
        c_plot = (c_all['GN2_truth_pt'] - c_all['truth_pt']) / c_all['truth_pt']
        b_plot = (b_all['GN2_truth_pt'] - b_all['truth_pt']) / b_all['truth_pt']

    else:
        q_plot = q_all[parameter]
        c_plot = c_all[parameter]
        b_plot = b_all[parameter]

    h_q = Histogram(values=q_plot, flavour='ujets', bins=np.linspace(xmin, xmax, 100))
    h_c = Histogram(values=c_plot, flavour='cjets', bins=np.linspace(xmin, xmax, 100))
    h_b = Histogram(values=b_plot, flavour='bjets', bins=np.linspace(xmin, xmax, 100))

    plot.add(h_q)
    plot.add(h_c)
    plot.add(h_b)

    plot.draw()
    plot.savefig(output_file)

