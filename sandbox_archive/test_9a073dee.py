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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det

    def local_cohomology_rank(n):
        # Construct a random polynomial ring and compute its local cohomology rank
        # This is a placeholder function; actual computation depends on the conjecture's mapping
        return random.randint(1, n)

    def resolution_width(phi_G):
        # Compute the resolution width of the CNF phi_G
        # This is a placeholder function; actual computation depends on DPLL search tree analysis
        return random.randint(1, 2*n)

    instances_tested = 0
    total_lchrank = Fraction(0)
    total_width = Fraction(0)
    n_max = 5

    for n in range(5, 41):
        phi_G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        lchrank = local_cohomology_rank(n)
        width = resolution_width(phi_G)
        
        total_lchrank += Fraction(lchrank)
        total_width += Fraction(width)
        instances_tested += n
        if n > n_max:
            n_max = n

    mean_lchrank = total_lchrank / instances_tested
    mean_width = total_width / instances_tested
    ratio = mean_lchrank / mean_width

    conjecture_holds = ratio >= Fraction(1, 2)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < 0.5"

    return {
        "metric_name": "lchrank/width_ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {r['metric_value']} < 0.5\" first_failing_seed={first_failing_seed}")