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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= 2
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] * pow(A[i][i], -1, 2)
            A[j][i:] = [(A[j][k] - factor * A[i][k]) % 2 for k in range(i, n)]
            b[j] = (b[j] - factor * b[i]) % 2
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) * pow(A[i][i], -1, 2)
    return x

def is_independent_system(A, b):
    try:
        gaussian_elimination(A, b)
        return True
    except ZeroDivisionError:
        return False

def permanent_matrix(n):
    if n == 0:
        return [[1]]
    P = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            P[i][j] = (i + j - 1) % 2
    return P

def symmetric_power(P, k):
    n = len(P)
    if k == 0:
        return [[1]]
    result = P.copy()
    for _ in range(1, k):
        new_result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for x in range(n):
                    new_result[i][j] += result[x][i] * P[j][x]
                    new_result[i][j] %= 2
        result = new_result
    return result

def trivial_representation_multiplicity(P, k):
    n = len(P)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    count = 0
    for b in itertools.product([0, 1], repeat=n):
        A = symmetric_power(P, k)
        if is_independent_system(A, list(b)):
            count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_multiplicity = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        P = permanent_matrix(n)
        multiplicity = trivial_representation_multiplicity(P, n)
        total_multiplicity += multiplicity
        instances_tested += 1

        # Minimal depth-3 circuit size upper bound (simplified example)
        min_circuit_size = n * math.log2(n)

        if multiplicity != min_circuit_size:
            conjecture_holds = False
            counterexample = f"n={n}, multiplicity={multiplicity}, expected={min_circuit_size}"

    return {
        "metric_name": "trivial_representation_multiplicity",
        "metric_value": total_multiplicity / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_multiplicity = sum(r["metric_value"] for r in results) / len(results)
    std_multiplicity = math.sqrt(sum((r["metric_value"] - mean_multiplicity)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_multiplicity} std={std_multiplicity} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        counterexample_desc = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")