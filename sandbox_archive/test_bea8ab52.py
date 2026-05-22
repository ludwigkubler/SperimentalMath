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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = 1
        U = gaussian_elimination(A)
        for i in range(n):
            det *= U[i][i]
        return det

    def tropical_discriminant(poly):
        n = len(poly) - 1
        A = [[-math.inf] * (n+1) for _ in range(n+1)]
        for i in range(n+1):
            for j in range(n+1):
                if i == j:
                    A[i][j] = poly[n-i]
                elif i < j:
                    A[i][j] = -math.inf
                else:
                    A[i][j] = max(A[i-1][j], A[i][j-1])
        return determinant(A)

    def random_dnf(n, k):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def characteristic_polynomial(dnf):
        n = len(dnf[0])
        poly = [1]
        for clause in dnf:
            term = 1
            for var in clause:
                term *= (1 + (-var))
            poly = [a + b * term for a, b in zip(poly, [0] * len(poly) + [term])]
        return poly

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        dnf = random_dnf(n, n)
        poly = characteristic_polynomial(dnf)
        disc = tropical_discriminant(poly)
        results.append(disc)

    mean_disc = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_disc) ** 2 for x in results) / len(results))
    
    conjecture_holds = all(disc >= n ** (3/2) for disc, n in zip(results, n_values)) and std_dev < 0.1 * n_values[0] ** (3/2)
    counterexample = "" if conjecture_holds else "n^3/2 bound violated"
    
    return {
        "metric_name": "Minimal Tropical Discriminant",
        "metric_value": mean_disc,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_disc = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_disc) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n^3/2 bound violated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")