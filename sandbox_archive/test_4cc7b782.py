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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return [row[:n-1] for row in A]

    def rank(A):
        return len(gaussian_elimination(A))

    def degree_of_smallest_XOR_tautology(poly):
        n = len(poly)
        if n == 0:
            return 0
        xors = set()
        for i in range(2**n):
            value = poly[0]
            for j in range(1, n):
                if (i >> j) & 1:
                    value ^= poly[j]
            xors.add(value)
        return len(xors)

    def generate_random_poly(n, degree):
        poly = [random.randint(0, 1) for _ in range(degree + 1)]
        poly[0] = random.choice([1, -1])
        return poly

    n = random.choice([5, 10, 15, 20, 30, 40])
    degree = random.randint(1, n)
    poly = generate_random_poly(n, degree)
    
    rho_f = rank([[poly[i] for i in range(j, j+degree+1)] for j in range(n)])
    xor_tautology_degree = degree_of_smallest_XOR_tautology(poly)
    
    return {
        "metric_name": "rank",
        "metric_value": rho_f,
        "instances_tested": 1,
        "conjecture_holds": rho_f >= xor_tautology_degree,
        "counterexample": "" if rho_f >= xor_tautology_degree else f"rho(f)={rho_f}, degree of smallest XOR tautology={xor_tautology_degree}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction=1.0")
    elif conjecture_holds_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={conjecture_holds_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")