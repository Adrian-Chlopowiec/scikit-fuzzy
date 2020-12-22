"""
defuzz.py : Various methods for defuzzification and lambda-cuts, to convert
            'fuzzy' systems back into 'crisp' values for decisions.
"""
import numpy as np

from .exceptions import EmptyMembershipError, InconsistentMFDataError
from ..image.arraypad import pad


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
    pass
