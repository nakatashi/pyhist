import argparse
import os
import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description="Histogram calculator.")
    parser.add_argument(
        "csv_file", help='.csv file containing data to be analyzed.')

    parser.add_argument("--row", help="")
    parser.add_argument("--col", help="")

    parser.add_argument("-s", action='store_true', help="Show graph")

    args = parser.parse_args()

    csv_filename = args.csv_file

    if args.col == None:
        col = 0
    else:
        col = int(args.col)

    if args.row == None:
        row = 0
    else:
        row = int(args.row)

    dat_array = load_data(csv_filename, row, col)

    threshold = 100

    bins = 'auto'

    hist_dat = calc_hist(dat_array, threshold, bins)

    dataFrame = pd.DataFrame(hist_dat)
    dataFrame.to_csv(add_suffix(csv_filename, "_hist" + str(row)), index=False, header=False)

    if args.s:
        plt.figure()
        plt.plot(hist_dat.T[0], hist_dat.T[1], 'o')
        
        plt.yscale("log")
        plt.ylabel("Frequency")
        plt.xlabel("Value")
        plt.xlim([0,1])
        plt.show()
    pass


def load_data(csv_filename, row, col):
    df = pd.read_csv(csv_filename, header=None, dtype='object')
    df_col = df[[col]]
    if row > 0:
        df_col = df_col.drop(range(row - 1))

    pos_array = numpy.array(df_col).astype(float)
    return pos_array


def calc_hist(dat_array, threshold, bin_cfg):
    H0 = numpy.histogram(dat_array, bins=bin_cfg)

    zeros = numpy.where(H0[0] < threshold)

    H = (numpy.delete(H0[0], zeros[0].tolist(), 0),
         numpy.delete(H0[1], zeros[0].tolist(), 0))

    return numpy.c_[H[1].tolist(), numpy.r_[0, H[0].tolist()]]

def add_suffix(filename, suffix):
    basename, ext = os.path.splitext(filename)
    return (basename+suffix+ext)
