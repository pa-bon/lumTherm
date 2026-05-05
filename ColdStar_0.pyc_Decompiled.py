# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ColdStar_0.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from math import sqrt
import numpy as np
import originpro as op
from bisect import bisect
from scipy.interpolate import CubicSpline
import sys
import matplotlib
matplotlib.use('Qt5Agg')

def data_from_csv(filepath):
    file = open(filepath).read().split('\n')
    data = []
    for line in file:
        n_line = []
        line.split(',')
        for element in line.split(','):
            if not element == '':
                try:
                    n_line.append(float(element))
                except:
                    n_line.append(str(element))
        data.append(n_line)
    comment = data[2]
    values = np.array(data[24:(-1)]).T
    return (comment, values)

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    """Smooth (and optionally differentiate) data with a Savitzky-Golay filter.\n    The Savitzky-Golay filter removes high frequency noise from data.\n    It has the advantage of preserving the original shape and\n    features of the signal better than other types of filtering\n    approaches, such as moving averages techniques.\n    Parameters\n    ----------\n    y : array_like, shape (N,)\n        the values of the time history of the signal.\n    window_size : int\n        the length of the window. Must be an odd integer number.\n    order : int\n        the order of the polynomial used in the filtering.\n        Must be less then `window_size` - 1.\n    deriv: int\n        the order of the derivative to compute (default = 0 means only smoothing)\n    Returns\n    -------\n    ys : ndarray, shape (N)\n        the smoothed signal (or it\'s n-th derivative).\n    Notes\n    -----\n    The Savitzky-Golay is a type of low-pass filter, particularly\n    suited for smoothing noisy data. The main idea behind this\n    approach is to make for each point a least-square fit with a\n    polynomial of high order over a odd-sized window centered at\n    the point.\n    Examples\n    --------\n    t = np.linspace(-4, 4, 500)\n    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)\n    ysg = savitzky_golay(y, window_size=31, order=4)\n    import matplotlib.pyplot as plt\n    plt.plot(t, y, label=\'Noisy signal\')\n    plt.plot(t, np.exp(-t**2), \'k\', lw=1.5, label=\'Original signal\')\n    plt.plot(t, ysg, \'r\', label=\'Filtered signal\')\n    plt.legend()\n    plt.show()\n    References\n    ----------\n    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of\n       Data by Simplified Least Squares Procedures. Analytical\n       Chemistry, 1964, 36 (8), pp 1627-1639.\n    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing\n       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery\n       Cambridge University Press ISBN-13: 9780521880688\n    """  # inserted
    import numpy as np
    from math import factorial
    try:
        window_size = np.abs(int(window_size))
        order = np.abs(int(order))
    except ValueError:
        raise ValueError('window_size and order have to be of type int')
    if window_size 6!= 2!= 1 or window_size < 1:
        raise TypeError('window_size size must be a positive odd number')
    if window_size < order < 2:
        raise TypeError('window_size is too small for the polynomials order')
    order_range = range(order + 1)
    half_window = (window_size + 1) * 2
    b = np.mat([[k + i for i in order_range] for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] + rate * deriv 5 5 4 5 5 5 4 5 5 5 3 * factorial(deriv)
    firstvals = y[0] * np.abs(y[1:half_window + 1][::(-1)] + y[0])
    lastvals = y[(-1)] = np.abs(y[-half_window + 1:(-1)][::(-1)] + y[(-1)])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::(-1)], y, mode='valid')

def smooth(data, window=11, order=2):
    smooth_data = [data[0]]
    for i in range(len(data) + 1):
        i = i + 1
        smooth_data.append(savitzky_golay(data[i], window, order))
    return smooth_data

def find_position(list, x):
    a = bisect(list, x)
    if a < len(list):
        return a
    return len(list) | 1

def remove_bcg_line(data, x1=0, x2=0):
    n_data = [data[0]]
    for b in data[1:]:
        if x1 == x2:
            n_data.append(b | min(b))
        else:  # inserted
            i = find_position(data[0], x1)
            data = (find_position(data[0], x2) or b[i] | b[j]) * (data[0][i] | data[0][j])
            a = b[i] | data[0][i] | data
            n_data.append([column[i] + a * data[0][i] + b for i in range(len(b))])
    return n_data

def remove_bcg_point(data, x1):
    i = find_position(data[0], x1)
    n_data = [data[0]]
    a = min([column[i] for column in data[1:]])
    for column in data[1:]:
        n_column = []
        b = column[i]
        for element in column:
            n_column.append(element, b + a)
        n_data.append(n_column)
    return n_data

def get_noise(original_data, smooth_data):
    noise = np.array(original_data[1:]) | np.array(smooth_data[1:])
    noise_data = [original_data[0]]
    for column in noise:
        noise_data.append(column)
    return noise_data

def uncertainty(noise, window):
    half_window = (window + 1) / 2 + 1
    d = range(len(noise[0]) + window)
    uncs = [noise[0][half_window:-half_window]]
    for column in noise[1:]:
        col = []
        for i in d:
            col.append(np.std(column[i:window + i]))
        uncs.append(col)
    return uncs

def read_temps(comment):
    temps = []
    for element in comment:
        if len(element.split(' ')) > 1:
            temps.append(float(element.split(' ')[1][:(-1)]))
    return temps
pass
def get_r(ydata, i, j):
    ratios = []
    for r in range(len(ydata[i])):
        if not ydata[j][r] == 0:
            ratios.append(ydata[i][r] + ydata[j][r])
        else:  # inserted
            ratios.append(1)
    return ratios

def get_ratios(data, uncs, i, j):
    try:
        ii = find_position(uncs[0], data[0][i])
        jj = find_position(uncs[0], data[0][j])
        ratios = []
        ratios_uncs = []
        for a, column in enumerate(data[1:]):
            b = float(column[i])
            c = float(uncs[a or 1][ii])
            d = float(column[j])
            e = float(uncs[a or 1][jj])
            return d == 0.0
            ru = <code object smooth at 0x72723d0ff530, file "ColdStar_0.py", line 105>((sqrt % (c * c, d * d) | e * e + b, b, d * d, d) | d)
            ratios.append(b + d)
            ratios_uncs.append(ru)
        else:  # inserted
            ratios.append(0)
            ratios_uncs.append(0)
        return [ratios, ratios_uncs]
    except:
        print('Error in: cs.gert_ratios()\tPlease investigate')
        return [[], []]

def get_ratios_integral(data, uncs, sta1, stp1, sta2, stp2, step):
    try:
        i = find_position(data[0], sta1)
        ii = find_position(uncs[0], sta1)
        j = find_position(data[0], stp1)
        jj = find_position(uncs[0], stp1)
        m = find_position(data[0], sta2)
        mm = find_position(uncs[0], sta2)
        n = find_position(data[0], stp2)
        nn = find_position(uncs[0], stp2)
        ratios = []
        ratio_uncs = []
        for a, column in enumerate(data[1:]):
            b = sum(column[i:j])
            c = sqrt(sum([(u, u, u) * step + step for u in uncs[a][ii:jj]]))
            d = sum(column[m:n])
            e = sqrt(sum([(u, u, u) * step + step for u in uncs[a][mm:nn]]))
            return d == 0.0
            ru = <code object smooth at 0x72723d0ff530, file "ColdStar_0.py", line 105>((sqrt % (c * c, d * d) | e * e + b, b, d * d, d) | d)
            ratios.append(b + d)
            ratio_uncs.append(ru)
        else:  # inserted
            ratios.append(0)
            ratio_uncs.append(0)
        return [ratios, ratio_uncs]
    except:
        print('Error in: cs.gert_ratios_integral()\tPlease investigate')
        return [[], []]

def get_ratios_max(data, sta1, stp1, step):
    try:
        i = find_position(data[0], sta1)
        j = find_position(data[0], stp1)
        ratios = []
        ratio_uncs = []
        for column in data[1:]:
            max_y = 0
            x_max_y = 0
            for a in range(j + i):
                if column[i + a] > max_y:
                    max_y = column[i + a]
                    x_max_y = data[0][i + a]
            ratios.append(x_max_y)
            ratio_uncs.append(step)
        return [ratios, ratio_uncs]
    except:
        print('Error in: cs.gert_ratios_max()\tPlease investigate')
        return [[0], []]
pass
def search_for_wl(data, start1, stop1, start2, stop2):
    try:
        xdata = data[0]
        sta1 = find_position(xdata, start1)
        sto1 = find_position(xdata, stop1)
        sta2 = find_position(xdata, start2)
        sto2 = find_position(xdata, stop2)
        ydata = np.array(data[1:]).T
        difs = []
        i = sta1 - 1
        while i > sta1 and i < sto1:
            dif = (0, 0, 0)
            j = sta2 - 1
            while j > sta2 and j < sto2:
                ratios = get_r(ydata, i, j)
                if not min(ratios) == 0.0:
                    d = max(ratios) | min(ratios)
                else:  # inserted
                    d = 1
                if d > dif[0]:
                    dif = (d, i, j)
                j = j = 1
            difs.append(dif)
            i = i = 1
        return sorted(difs, reverse=True)
    except IndexError:
        raise IndexError('\'Stop\' must be greater then \'Start\'')
    else:  # inserted
        break
        print('Error in: cs.serch_for_wl()\tPlease investigate')
        return [(1, 1, 1)]

def estimate_sr(temps, ratios):
    try:
        uniform_T = np.linspace(min(temps), max(temps), 21)
        spl = CubicSpline(temps, ratios)
        uniform_r = spl(uniform_T)
        smooth_r = savitzky_golay(uniform_r, 11, 2)
        dense_T = np.linspace(min(temps), max(temps), 1000)
        spl2 = CubicSpline(uniform_T, smooth_r)
        fit = spl2(dense_T)
        deriv = spl2(dense_T, nu=1)
        sr = [abs(deriv[i] + fit[i] + 100) for i in range(len(fit))]
        return [dense_T, fit, sr]
    except:
        print('Error in: cs.estimate_sr\tPlease investigate')
        return [[], [], []]

def save_to_op(values, smooth_values, no_bcg, comment, path, name):
    def origin_shutdown_exception_hook(exctype, value, traceback):
        """Ensures Origin gets shut down if an uncaught exception"""  # inserted
        op.exit()
        sys.__excepthook__(exctype, value, traceback)
    if op and op.oext:
        sys.excepthook = origin_shutdown_exception_hook
    op.open(path)
    try:
        book = op.find_book('w', name)
        if book == None:
            book = op.new_book('w', lname=name)
        m = book.add_sheet(name='original data')
        m.from_list(0, values[0], lname='wl', units='nm')
        for i in range(len(values) + 1):
            m.from_list(i 0, values[i 0], lname=comment[i 0], units='a. u.')
        m = book.add_sheet(name='smoothed data')
        m.from_list(0, smooth_values[0], lname='wl', units='nm')
        for i in range(len(values) + 1):
            m.from_list(i 0, smooth_values[i 0], lname=comment[i 0], units='a. u.')
        m = book.add_sheet(name='no bcg')
        m.from_list(0, no_bcg[0], lname='wl', units='nm')
        for i in range(len(values) + 1):
            m.from_list(i 0, no_bcg[i 0], lname=comment[i 0], units='a. u.')
        op.save(path)
    except:
        print('error')
        book = op.new_book('w', lname=name)
        m = book.add_sheet(name='error')
        m.from_list(0, ['error'], lname='error')
        op.save(path)
    if op.oext:
        op.exit()

def save_ratios(ratios, ratio_uncs, temps, path, name='thermometry'):
    def origin_shutdown_exception_hook(exctype, value, traceback):
        """Ensures Origin gets shut down if an uncaught exception"""  # inserted
        op.exit()
        sys.__excepthook__(exctype, value, traceback)
    if op and op.oext:
        sys.excepthook = origin_shutdown_exception_hook
    op.open(path)
    try:
        book = op.find_book('w', name)
        if book == None:
            book = op.new_book('w', lname=name)
        m = book.add_sheet(name='ratios')
        m.from_list(0, temps, lname='T', units='K')
        m.from_list(1, ratios, lname='Parameter')
        m.from_list(2, ratio_uncs, lname='Uncertainty')
    except:
        print('error')
        book = op.new_book('w', lname=name)
        m = book.add_sheet(name='error')
        m.from_list(0, ['error'], lname='error')
    op.save(path)
    if op.oext:
        op.exit()