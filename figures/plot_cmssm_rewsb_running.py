"""Plot running of CMSSM parameters relevant to EWSB."""

import argparse
import numpy as np
import matplotlib.pyplot as plt

SCALE_DATA = "scale"
MU_DATA = "Mu"
BMU_DATA = "BMu"
MHU2_DATA = "mHu2"
MHD2_DATA = "mHd2"

def get_plot_data(mu_data, mhu2_data, mhd2_data):
    """Get parameter combinations to plot."""
    hu_data = { "label":
                r"$\sign(m_{H_u}^2 + |\mu|^2) \sqrt{|m_{H_u}^2 + |\mu|^2|}$",
                "data": np.sign(mhu2_data) * np.sqrt(np.abs(mhu2_data))
              }
    hd_data = { "label":
                r"$\sign(m_{H_d}^2 + |\mu|^2) \sqrt{|m_{H_d}^2 + |\mu|^2|}$",
                "data": np.sign(mhd2_data) * np.sqrt(np.abs(mhd2_data))
              }

    hu_combined = mhu2_data + mu_data * mu_data
    hd_combined = mhd2_data + mu_data * mu_data

    hu_data["data"] = np.sign(hu_combined) * np.sqrt(np.abs(hu_combined))
    hd_data["data"] = np.sign(hd_combined) * np.sqrt(np.abs(hd_combined))

    return (hu_data, hd_data)

def plot_running(scale_data, mu_data, bmu_data, mhu2_data, mhd2_data,
                 outfile=""):
    """Plot a line plot of the CMSSM EWSB sector running."""
    fig = plt.figure(figsize=(5,4))
    plt.gcf().subplots_adjust(left=0.2, bottom=0.15)

    plt.rc("text", usetex=True)
    plt.rc("font", family="serif", weight="normal")
    plt.rcParams["text.latex.preamble"] = [
        "\\usepackage{amsmath}\n\\DeclareMathOperator{\\sign}{sign}"]

    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.tick_params(direction="in", which="both")
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    hu_data, hd_data = get_plot_data(mu_data, mhu2_data, mhd2_data)
    b_data = np.sign(bmu_data) * np.sqrt(np.abs(bmu_data))

    plt.semilogx(scale_data, hu_data["data"], "r-", label=hu_data["label"])
    plt.semilogx(scale_data, hd_data["data"], "g--", label=hd_data["label"])
    plt.semilogx(scale_data, b_data, "b:", label=r"$\sign(B\mu) \sqrt{|B\mu|}$")

    plt.xlabel(r"$Q\;/\;\mathrm{GeV}$")
    plt.ylabel(r"$m\;/\;\mathrm{GeV}$")
    plt.title(
        r"Valid EWSB: $(m_{H_d}^2 + |\mu|^2) (m_{H_u}^2 + |\mu|^2) < (B\mu)^2$",
        size=11)

    plt.ylim([-800,800])
    plt.grid(color="gray", linestyle=":", linewidth=0.2,
            dashes=(0.5,1.5))

    leg = plt.legend(numpoints=1, prop={"size": 11},
                    loc="lower right")
    leg.get_frame().set_alpha(1.0)
    leg.get_frame().set_edgecolor("black")

    if outfile:
        plt.savefig(outfile)
    plt.close(fig)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Plot running of CMSSM parameters relevant to EWSB.")
    parser.add_argument("datafile", help="datafile to plot from")
    parser.add_argument("--output-file", dest="outfile",
            help="name to save plot with")
    args = parser.parse_args()
    return (args.datafile, args.outfile)

def main():
    """Plot running of CMSSM parameters relevant to EWSB."""
    datafile, outfile = parse_args()
    data = np.genfromtxt(datafile, names=True,
                         usecols=[SCALE_DATA, MU_DATA, BMU_DATA,
                                  MHU2_DATA, MHD2_DATA])
    plot_running(data[SCALE_DATA], data[MU_DATA], data[BMU_DATA],
                 data[MHU2_DATA], data[MHD2_DATA], outfile)

if __name__ == "__main__":
    main()

