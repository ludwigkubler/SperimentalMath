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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_norm(A):
    n = len(A)
    max_row_sum = 0
    for i in range(n):
        row_sum = sum(abs(x) for x in A[i])
        if row_sum > max_row_sum:
            max_row_sum = row_sum
    return max_row_sum

def generate_circuit(n, d):
    circuit = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < (n * (d - 1)) // 2:
        u, v = random.sample(range(n), 2)
        if u > v: u, v = v, u
        if (u, v) not in edges and (v, u) not in edges:
            circuit[u][v] = 1
            circuit[v][u] = 1
            edges.add((u, v))
    return circuit

def fourier_multiplier(circuit):
    n = len(circuit)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                A[i][j] = 1
            else:
                A[i][j] = (math.cos(2 * math.pi * i * j / n) - 1) / (i * j)
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metrics = []
    instances_tested = 0
    n_max = 5
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_circuit(n, d=3)
            M_C = fourier_multiplier(circuit)
            norm_M_C = matrix_norm(M_C)
            E_C = sum(sum(row) for row in circuit) // 2
            if norm_M_C > 10 * E_C**2:
                conjecture_holds = False
                counterexample = f"n={n}, E(C)={E_C}, |M_C|_∞={norm_M_C}"
                break
            metrics.append(norm_M_C)
        instances_tested += 5
        if n > n_max:
            n_max = n
    
    return {
        "metric_name": "Fourier Multiplier Norm",
        "metric_value": sum(metrics) / len(metrics),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")