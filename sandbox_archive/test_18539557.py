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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matroid_connectivity(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(n):
        if any(all(A[j][k] == 0 for k in range(i)) for j in range(m)):
            continue
        rank += 1
        for j in range(m):
            if A[j][i]:
                for k in range(i + 1, n):
                    A[j][k] = (A[j][k] - A[j][i] * A[i][k]) % 2
    return rank

def is_3sat_satisfiable(phi):
    # Placeholder implementation of a SAT solver
    # This is a very naive and inefficient implementation for testing purposes
    n = len(phi)
    variables = [0] * n
    while True:
        if all(any(lit in clause for lit in clause) or not any(lit in clause for lit in clause) for clause in phi):
            return True
        if all(variables[i] != -1 for i in range(n)):
            return False
        for i in range(n):
            if variables[i] == -1:
                variables[i] = 0
                break
        else:
            variables = [-1] * n
        for i in range(n):
            if variables[i] == 0:
                variables[i] = 1
                break

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        for _ in range(30):
            phi = [[random.choice([-1, 1]) * random.randint(1, n) for _ in range(n)] for _ in range(n)]
            A = [[int(lit != 0) for lit in clause] for clause in phi]
            connectivity = matroid_connectivity(A)
            if not is_3sat_satisfiable(phi):
                continue
            instances_tested += 1
            if connectivity != math.log2(n + 1):
                conjecture_holds = False
                counterexample = f"n={n}, connectivity={connectivity}"
        results.append({
            "metric_name": "matroid_connectivity",
            "metric_value": connectivity,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    mean_value = sum(res["metric_value"] for res in all_results) / len(all_results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in all_results) / len(all_results))
    support_fraction = sum(1 for res in all_results if res["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in all_results):
        first_failing_seed = next(seed for seed, res in zip(seeds, all_results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")