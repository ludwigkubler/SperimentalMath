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
    
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(b)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(i, n + 1):
                M[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(i, n + 1):
                        M[j][k] -= factor * M[i][k]
        return [row[-1] for row in M]
    
    def generate_lattice(n):
        lattice = []
        for i in range(2**n):
            point = [int(x) for x in bin(i)[2:].zfill(n)]
            lattice.append(point)
        return lattice
    
    def circuit_entanglement_complexity(n):
        # Simplified model of entanglement complexity
        return n * (n - 1) // 2
    
    def minimal_orbit_diameter(lattice):
        n = len(lattice[0])
        distances = []
        for i in range(len(lattice)):
            for j in range(i + 1, len(lattice)):
                dist = sum(abs(x - y) for x, y in zip(lattice[i], lattice[j]))
                distances.append(dist)
        return min(distances)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        lattice = generate_lattice(n)
        gamma_n = circuit_entanglement_complexity(n)
        orbit_diameter = minimal_orbit_diameter(lattice)
        results.append((orbit_diameter, gamma_n))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    orbit_diameters = [r[0] for r in results]
    gamma_ns = [r[1] for r in results]
    
    mean_orbit_diameter = sum(orbit_diameters) / len(orbit_diameters)
    mean_gamma_n = sum(gamma_ns) / len(gamma_ns)
    
    covariance = sum((orbit_diameters[i] - mean_orbit_diameter) * (gamma_ns[i] - mean_gamma_n) for i in range(len(results))) / (len(results) - 1)
    variance_orbit_diameter = sum((orbit_diameters[i] - mean_orbit_diameter) ** 2 for i in range(len(results))) / (len(results) - 1)
    variance_gamma_n = sum((gamma_ns[i] - mean_gamma_n) ** 2 for i in range(len(results))) / (len(results) - 1)
    
    correlation_coefficient = covariance / math.sqrt(variance_orbit_diameter * variance_gamma_n)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / (len(results) - 1))
    
    conjecture_holds_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{0.8}\" first_failing_seed={first_failing_seed}")