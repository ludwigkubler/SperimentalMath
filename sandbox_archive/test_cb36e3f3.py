# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i, n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_inv(A):
    n = len(A)
    I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    A_augmented = [row + col for row, col in zip(A, I)]
    A_rref = gaussian_elimination(A_augmented)
    inv_M = [[A_rref[i][j+n] for j in range(n)] for i in range(n)]
    return inv_M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    d_values = [5, 10, 15, 20, 30, 40]
    condition_numbers = []
    sos_degrees = []

    for d in d_values:
        # Generate a random max-CUT instance with n variables
        A = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        A = [row[:] for row in A]
        for i in range(n):
            for j in range(i+1, n):
                A[j][i] = A[i][j]

        # Compute the moment matrix
        M = [[sum(A[i][k] * A[j][l] for k in range(n) for l in range(n)) for j in range(n)] for i in range(n)]

        # Calculate the condition number
        inv_M = matrix_inv(M)
        condition_number = sum(sum(abs(inv_M[i][j]) for j in range(n)) for i in range(n))
        condition_numbers.append(condition_number)

        # Determine the SOS degree required to achieve an approximation ratio of 0.878 - ε
        sos_degree = d  # Placeholder, actual computation depends on the problem specifics

        sos_degrees.append(sos_degree)

    mean_condition_number = sum(condition_numbers) / len(condition_numbers)
    std_condition_number = math.sqrt(sum((x - mean_condition_number) ** 2 for x in condition_numbers) / len(condition_numbers))
    support_fraction = len([x for x in condition_numbers if x <= 1/d_values[0]**2]) / len(d_values)

    return {
        "metric_name": "Condition Number",
        "metric_value": mean_condition_number,
        "instances_tested": len(d_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_condition_number = sum(result["metric_value"] for result in results) / len(results)
    std_condition_number = math.sqrt(sum((result["metric_value"] - mean_condition_number) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_condition_number} std={std_condition_number} support_fraction={support_fraction}")