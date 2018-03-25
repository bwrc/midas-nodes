#!/usr/bin/env python

import scipy
import scipy.signal
import numpy

# -----------------------------------------------------------------------------
# Time domain analysis functions for IBI series
# -----------------------------------------------------------------------------


def hrv_mean_ibi(x, fs=500):
    """ average interbeat interval length """
    rr = detect_r_peaks(x['data'][0], fs)
    return numpy.mean(rr)


def hrv_mean_hr(x, fs=500):
    """ average heart rate """
    rr = detect_r_peaks(x['data'][0], fs)
    return 6e4 / numpy.mean(rr)


def hrv_rmssd(x):
    """ root mean square of successive differences """
    return scipy.sqrt(scipy.sum(scipy.diff(x)**2) / (len(x) - 1))


def hrv_var(x):
    """ variance of the interbeat interval lengths """
    return scipy.var(x)


def hrv_std(x):
    """ standard deviation of the interbeat interval lengths """
    return scipy.std(x)


def hrv_pnnx(ibi, p=50):
    """ percentage of normal-to-normal intervals exceeding x milliseconds """
    return 100 * scipy.sum(abs(scipy.diff(ibi)) >= float(p)) / len(ibi)

# -----------------------------------------------------------------------------
# Frequency domain analysis functions for IBI series
# -----------------------------------------------------------------------------


def bandpower(f, Pxx, fmin, fmax):
    """ integrate the power spectral density between fmin and fmax
        using the trapezoidal method
    """
    ind_min = scipy.argmax(f > fmin) - 1
    ind_max = scipy.argmax(f > fmax) - 1
    return scipy.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])


def hrv_lomb(ibi, fmin, fmax):
    """ Calculate the power in the given frequency band using the Lomb-Scargle
        periodogram.

    Args:
          ibi: the IBI series
        fmin : lower frequency of the band being considered
        fmax : upper frequency of the band being considered
    """

    ibi = scipy.array(ibi)
    ibi_t = scipy.concatenate([[0], scipy.cumsum(ibi[:-1])])

    N = 512.0
    f = scipy.linspace(1.0 / N, 40.0, N)
    p = scipy.signal.lombscargle(ibi_t, ibi, f)
    return bandpower(f, p, fmin, fmax)

# -----------------------------------------------------------------------------
# R-peak detection from an ECG signal
# -----------------------------------------------------------------------------


def moving_average(x, n=10):
    return numpy.convolve(x, numpy.ones((n,)) / n, mode='valid')


def adjust_indices(ind_start, ind_stop):
    if (ind_stop[0] <= ind_start[0]):
        ind_stop = ind_stop[1:]

    n_min = numpy.min([len(ind_start), len(ind_stop)])
    ind_start = ind_start[:n_min]
    ind_stop = ind_stop[:n_min]

    return ind_start, ind_stop


def find_r_peak(data, ind_r, ind_f):
    rph = [0] * len(ind_r)
    rpp = [0] * len(ind_r)

    for i in range(len(ind_r)):
        # print(str(ind_r[i]), '   ---  ', str(ind_f[i]))
        rph[i] = max(data[ind_r[i]:ind_f[i]])
        rpp[i] = numpy.argmax(data[ind_r[i]:ind_f[i]]) + ind_r[i] - 1
    return rph, rpp


def detect_r_peaks(data, fs=500):
    """ Calculate peak stuff from ecg stuff. """
    data_orig = numpy.copy(data)
    tmp       = scipy.signal.medfilt(data, 31)
    data      = data - tmp

    thr       = 0.70 * numpy.max(data)

    # Make the signal binary
    data[data < thr] = 0
    data[data >= thr] = 1

    # Find rising and falling edges used to window the R-peak
    ind_rising  = numpy.where(numpy.diff(data) == 1)[0]
    ind_falling = numpy.where(numpy.diff(data) == -1)[0]

    ind_rising, ind_falling = adjust_indices(ind_rising, ind_falling)

    for i in range(1, len(ind_rising)):
        ind_rising[i]  = ind_rising[i] - round(fs / 4)
        ind_falling[i] = ind_falling[i] + round(fs /4)

    # Determine the R-peak for each pair of rising and falling edges
    rph, rpp = find_r_peak(data_orig, ind_rising, ind_falling)

    rr = 1000 * (numpy.diff(rpp) / fs)
    return rr


# -----------------------------------------------------------------------------
