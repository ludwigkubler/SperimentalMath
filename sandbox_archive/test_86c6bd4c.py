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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def tensor_rank(permutation):
    n = len(permutation)
    identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    tensor = []
    for p in permutation:
        row = [identity[i][p-1] for i in range(n)]
        tensor.append(row)
    return max(gaussian_elimination(tensor, [1]*n))

def boolean_function_to_permutation(f):
    n = len(f)
    sign = [f(i) * 2 - 1 for i in range(1 << n)]
    permutation = sorted(range(1 << n), key=lambda x: sign[x])
    return permutation

def min_representation_rank(permutation):
    n = len(permutation)
    identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    tensor = []
    for p in permutation:
        row = [identity[i][p-1] for i in range(n)]
        tensor.append(row)
    return max(gaussian_elimination(tensor, [1]*n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    rho_values = []
    tau_values = []
    
    for n in n_values:
        f = lambda x: random.choice([True, False])
        permutation = boolean_function_to_permutation(f)
        rho = min_representation_rank(permutation)
        tau = tensor_rank(permutation)
        rho_values.append(rho)
        tau_values.append(tau)
    
    correlation_coefficient = sum((rho - mean_rho) * (tau - mean_tau) for rho, tau in zip(rho_values, tau_values)) / len(n_values)
    mean_rho = sum(rho_values) / len(rho_values)
    mean_tau = sum(tau_values) / len(tau_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")