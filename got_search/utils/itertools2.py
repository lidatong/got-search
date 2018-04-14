from itertools import zip_longest
from typing import Iterable, Optional, Tuple, Container
from bisect import bisect_left

from got_search.utils.functools2 import identity
from got_search.utils.typevars import A


def grouper(xs: Iterable[A], n: int = 2, fillvalue=None) -> Iterable[Tuple[A]]:
    its = [iter(xs)] * n
    yield from zip_longest(*its, fillvalue=fillvalue)


def find(xs: Container[A], key=identity, is_sorted=False) -> Optional[A]:
    # TODO sorted case
    for x in xs:
        if key(x):
            return x
    return None
