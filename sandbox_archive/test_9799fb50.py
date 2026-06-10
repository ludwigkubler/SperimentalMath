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
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def rank(A):
        rref = gaussian_elimination(A)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def random_communication_protocol(n):
        protocol = []
        for _ in range(n):
            protocol.append(random.randint(1, n))
        return protocol

    def moduli_space(protocol):
        n = len(protocol)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i][j] = Fraction(1)
                elif abs(protocol[i] - protocol[j]) <= 1:
                    A[i][j] = Fraction(1)
        return A

    def hcr(phi):
        n = len(phi)
        moduli = moduli_space(phi)
        return rank(moduli)

    def rvar(phi):
        n = len(phi)
        moduli = moduli_space(phi)
        mean = sum(sum(row) for row in moduli) / (n * n)
        variance = sum((moduli[i][j] - mean) ** 2 for i in range(n) for j in range(n)) / (n * n)
        return variance

    instances_tested = 0
    hcr_values = []
    rvar_values = []

    for _ in range(30):
        phi = random_communication_protocol(random.randint(5, 40))
        hcr_val = hcr(phi)
        rvar_val = rvar(phi)
        if hcr_val > 0 and rvar_val > 0:
            instances_tested += 1
            hcr_values.append(hcr_val)
            rvar_values.append(rvar_val)

    if instances_tested == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }

    hcr_mean = sum(hcr_values) / instances_tested
    rvar_mean = sum(rvar_values) / instances_tested
    covariance = sum((hcr_val - hcr_mean) * (rvar_val - rvar_mean) for hcr_val, rvar_val in zip(hcr_values, rvar_values)) / instances_tested
    hcr_std = math.sqrt(sum((hcr_val - hcr_mean) ** 2 for hcr_val in hcr_values) / instances_tested)
    rvar_std = math.sqrt(sum((rvar_val - rvar_mean) ** 2 for rvar_val in rvar_values) / instances_tested)
    correlation = covariance / (hcr_std * rvar_std)

    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")