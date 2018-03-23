"""Plot running of CMSSM gauge couplings."""

import argparse
import numpy as np
import matplotlib.pyplot as plt

SCALE_DATA = "scale"
G1_DATA = "g1"
G2_DATA = "g2"
G3_DATA = "g3"

def plot_running(scale_data, g1_data, g2_data, g3_data, outfile=""):
    """Plot a line plot of the CMSSM gauge coupling running."""
    fig = plt.figure(figsize=(5,4))
    plt.gcf().subplots_adjust(left=0.2,bottom=0.15)

    plt.rc("text", usetex=True)
    plt.rc("font", family="serif", weight="normal")
    plt.rcParams["text.latex.preamble"] = [r"\usepackage{amsmath}"]

    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.tick_params(direction="in", which="both")
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    plt.semilogx(scale_data, g1_data, "r-", label="$g_1$")
    plt.semilogx(scale_data, g2_data, "g--", label="$g_2$")
    plt.semilogx(scale_data, g3_data, "b:", label="$g_3$")

    plt.xlabel(r"$Q\;/\;\mathrm{GeV}$")
    plt.grid(color="gray", linestyle=":", linewidth=0.2,
            dashes=(0.5,1.5))

    leg = plt.legend(numpoints=1, prop={"size": 12},
                    loc="upper right")
    leg.get_frame().set_alpha(1.0)
    leg.get_frame().set_edgecolor("black")

    if outfile:
        plt.savefig(outfile)
    plt.close(fig)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
            description="Plot running of CMSSM gauge couplings")
    parser.add_argument("datafile", help="datafile to plot from")
    parser.add_argument("--output-file", dest="outfile",
            help="name to save plot with")
    args = parser.parse_args()
    return (args.datafile, args.outfile)

def main():
    """Plot running of CMSSM gauge couplings."""
    datafile, outfile = parse_args()
    data = np.genfromtxt(datafile, names=True,
                         usecols=[SCALE_DATA, G1_DATA, G2_DATA, G3_DATA])
    plot_running(data[SCALE_DATA], data[G1_DATA], data[G2_DATA],
                 data[G3_DATA], outfile)

if __name__ == "__main__":
    main()
