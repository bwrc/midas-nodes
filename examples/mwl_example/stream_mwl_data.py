#!/usr/bin/env python3

import time
import pylsl as lsl


def read_data(fname):
    data = open(fname, "r").readlines()
    data = [float(i.strip()) for i in data]
    return data


def equalize(x, n):
    return x[:(n-1)]

# read the data
d_ecg = read_data("data/data_ecg.csv")
d_fz = read_data("data/data_eeg_fz.csv")
d_pz = read_data("data/data_eeg_pz.csv")

# make the data equally long
dset = (d_ecg, d_fz, d_pz)
n = min(list(map(len, dset)))
d_ecg, d_fz, d_pz = [equalize(d, n) for d in dset]

# create outlets
info_ecg = lsl.StreamInfo('n1_ecg', 'ECG', 1, 100, 'float32', 'ecg123')
info_eeg = lsl.StreamInfo('n1_eeg', 'EEG', 2, 100, 'float32', 'eeg123')
outlet_ecg = lsl.StreamOutlet(info_ecg)
outlet_eeg = lsl.StreamOutlet(info_eeg)

# stream the data
print("streaming data")
i = 0
while True:
    outlet_ecg.push_sample([d_ecg[i]])
    outlet_eeg.push_sample([d_fz[i], d_pz[i]])
    time.sleep(1.0 / 100.0)
    i += 1
    if i >= len(d_ecg) or i >= len(d_fz) or i >= len(d_pz):
        i = 0
