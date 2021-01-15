"""
defuzz.py : Various methods for defuzzification and lambda-cuts, to convert
            'fuzzy' systems back into 'crisp' values for decisions.
"""
import numpy as np

from .exceptions import EmptyMembershipError, InconsistentMFDataError
from ..image.arraypad import pad

EPSILON = 1e-6


def defuzz(x, mfx):
    """
    Defuzzification of a membership function, returning a defuzzified value
    of the function at x using Karnik-Mendel Algorithm.

    Parameters
    ----------
    x : 1d array or iterable, length N
        Independent variable.
    mfx : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    u : float or int
        Defuzzified result.

    Raises
    ------
    - EmptyMembershipError : When the membership function area is empty.
    - InconsistentMFDataError : When the length of the 'x' and the fuzzy
        membership function arrays are not equal.
    """

    teta = (mfx[0] + mfx[1]) / 2.0
    yL, L = __find_y(x, teta.copy(), mfx[1], mfx[0])
    yR, R = __find_y(x, teta.copy(), mfx[0], mfx[1])

    # yL = __calc_y_val(x, L, mfx[1], mfx[0])
    # yR = __calc_y_val(x, R, mfx[0], mfx[1])
    return (yL + yR) / 2


def __find_y(universe, teta, first_mf, second_mf):
    def calc_c_second(new_teta, c):
        k = 0
        for i in universe:
            if i >= c:
                k -= 1
                break
            k += 1

        for i, l_val, r_val in zip(range(0, len(first_mf)), first_mf, second_mf):
            if i <= k:
                new_teta[i] = l_val
            else:
                new_teta[i] = r_val

        return np.average(universe, weights=new_teta), new_teta, k

    cprim = np.average(universe, weights=teta)
    csecond, teta, k = calc_c_second(teta, cprim)
    
    i = 0
    while abs(csecond - cprim) >= EPSILON:
        cprim = csecond
        csecond, teta, k = calc_c_second(teta, cprim)
        i += 1
        if i > 1000:
            raise Exception("Probably endless loop in defuzz")

    return csecond, k


def __calc_y_val(universe, breakpoint, first_mf, second_mf):
    def sum_of_series(array, mf, start, end):
        acc = 0
        for i in range(start, end):
            acc += array[i] * mf[i]
        return acc

    return ((sum_of_series(universe, first_mf, 0, breakpoint + 1)
             + sum_of_series(universe, second_mf, breakpoint + 1, len(universe)))
            / (sum_of_series(np.ones_like(universe), first_mf, 0, breakpoint + 1)
               + sum_of_series(np.ones_like(universe), second_mf, breakpoint + 1, len(universe))))
