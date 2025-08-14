from puma import Roc, RocPlot
from ftag import Flavours
from ftag.utils import calculate_rejection, get_discriminant # type: ignore
import h5py
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('flavour', choices=['u', 'c', 'b'])

args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file
flavour = args.flavour

with h5py.File(input_file, 'r') as h5file:
    jets = h5file['jets'][:]

u_mask = jets['flavour_label'] == 0
c_mask = jets['flavour_label'] == 1
b_mask = jets['flavour_label'] == 2

eff = np.linspace(0, 1, 40)
y = 1/eff[1:]

roc1_dict = {
    'b': ['ujets', 'bjets', 'tab:green', 'Light jets'],
    'c': ['ujets', 'cjets', 'tab:green', 'Light jets']
}

roc2_dict = {
    'b': ['cjets', 'bjets', 'tab:orange', 'c jets'],
    'c': ['bjets', 'cjets', 'tab:blue', 'b jets']
}

label_dict = {
    'b': '$b$-jet efficiency',
    'c': '$c$-jet efficiency'
}

if flavour == 'b':

    discs = get_discriminant(
        jets=jets,
        tagger='GN2',
        signal=Flavours['bjets'],
        flavours=Flavours.by_category('single-btag'),
        fraction_values={'fc': 0.2, 'fu': 0.8, 'ftau': 0}
    )

    rej_1 = calculate_rejection(discs[b_mask], discs[u_mask], eff)
    rej_2 = calculate_rejection(discs[b_mask], discs[c_mask], eff)

elif flavour == 'c':

    discs = get_discriminant(
    jets=jets,
    tagger='GN2',
    signal=Flavours['cjets'],
    flavours=Flavours.by_category('single-btag'),
    fraction_values={'fb': 0.3, 'fu': 0.7, 'ftau': 0}
    )

    rej_1 = calculate_rejection(discs[c_mask], discs[u_mask], eff)
    rej_2 = calculate_rejection(discs[c_mask], discs[b_mask], eff)

roc_1 = Roc(
    sig_eff=eff,
    bkg_rej=rej_1,
    rej_class=roc1_dict[flavour][0],
    signal_class=roc1_dict[flavour][1],
    colour=roc1_dict[flavour][2],
    label=roc1_dict[flavour][3],
    linestyle='solid'
)

roc_2 = Roc(
    sig_eff=eff,
    bkg_rej=rej_2,
    rej_class=roc2_dict[flavour][0],
    signal_class=roc2_dict[flavour][1],
    colour=roc2_dict[flavour][2],
    label=roc2_dict[flavour][3],
    linestyle='solid'
)

myplot = RocPlot(
    ylabel='Background Rejection',
    xlabel=label_dict[flavour],
    figsize=(4.8, 3.6),
    n_ratio_panels=0,
    atlas_brand = 'Muon Collider'
)

# plot.make_linestyle_legend(linestyles=['solid', 'dashdot'], labels=['u jets', 'c jets'], loc='upper right')

myplot.add_roc(roc_1)
myplot.add_roc(roc_2)
myplot.draw()

fig = myplot.fig
ax = myplot.axis_top

if ax.get_legend() is not None:
    ax.get_legend().remove()

line, = ax.plot(eff[1:], y, 'k--', linewidth=2, label='Random classifier')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels)

# myplot.savefig(output_file)
fig.savefig(output_file, dpi=200)
plt.close(fig)
