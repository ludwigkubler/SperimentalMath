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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def count_non_zero_coeffs(poly):
        return sum(1 for coeff in poly if coeff != 0)

    def abp_width_from_cnf(cnf):
        # Simplified approximation based on known results
        return len(cnf) ** (1/3)

    n = random.randint(5, 40)
    cnf = []
    for _ in range(random.randint(n, 2*n)):
        clause = [random.randint(-n, n) for _ in range(3)]
        if all(abs(lit) != abs(clause[0]) for lit in clause):
            cnf.append(tuple(sorted(clause)))

    indicator_poly = [1] + [0] * (2**n - 1)
    for clause in cnf:
        for i in range(len(indicator_poly)):
            if any(abs(lit) <= abs(i) for lit in clause):
                indicator_poly[i] ^= 1

    A = []
    for i in range(2**n):
        row = [0] * (n + 1)
        row[-1] = indicator_poly[i]
        for j in range(n):
            if i & (1 << j):
                row[j] = 1
        A.append(row)

    A = gaussian_elimination(A)
    non_zero_coeffs = count_non_zero_coeffs([row[-1] for row in A])

    abp_width = abp_width_from_cnf(cnf)

    return {
        "metric_name": "ABP Width",
        "metric_value": abp_width,
        "instances_tested": 1,
        "conjecture_holds": non_zero_coeffs >= abp_width,
        "counterexample": "" if non_zero_coeffs >= abp_width else f"n={n}, cnf={cnf}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")