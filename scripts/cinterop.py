# interoperating with handrolled C libraries
import timeit

import numpy as np
from numba import jit


def factorial(n: int) -> float:  # tested, works correctly
    """
    returns the factorial of n (!n)
    """
    if n < 0:
        raise ValueError("factorial() does not accept negative inputs!")
    if (not n) or (n == 1):
        return 1.0000
    result: float = 1.0000
    for i in range(2, n + 1):
        result *= i
    return result


@jit(nopython=True, inline="always", boundscheck=False, fastmath=True, parallel=False)
def factorial_opt(n: np.uint32) -> np.float64:
    """
    returns the factorial of n (!n)
    """
    if n < 0:
        return np.float64(0.0000)
    if (not n) or (n == 1):
        return np.float64(1.0000)
    result: np.float64 = np.float64(1.0000)
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    # assert factorial(0) == 1.0000
    # assert factorial(1) == 1.0000
    # assert factorial(4) == 24.0000
    # assert factorial(6) == 720.0000
    # assert factorial(7) == 5040.0000
    # assert factorial(10) == 3_628_800.0000
    # assert factorial(23) == 25_852_016_738_884_976_640_000.0000
    pass

    numbers: tuple[int, ...] = tuple(range(0, 26))
    results: tuple[float, ...] = tuple(factorial(i) for i in numbers)
    tm = timeit.timeit(
        stmt=f"res: tuple[float, ...] = tuple(factorial(i) for i in numbers)",
        number=100,
        globals={"numbers": numbers, "factorial": factorial},
    )
    print(f"{tm:3.8f}")
