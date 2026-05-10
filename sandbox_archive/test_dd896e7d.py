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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def spectral_norm(M):
    n = len(M)
    v = [Fraction(1, math.sqrt(n)) for _ in range(n)]
    for _ in range(100):  # Power iteration
        v = [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
        v = [x / sum(v[j]**2 for j in range(n))**0.5 for x in v]
    return max(abs(x) for x in v)

def communication_complexity_lower_bound(n, epsilon):
    return Fraction(math.log(1 / epsilon), math.log(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    d = 2
    c = Fraction(1, 10)  # Hypothetical constant for demonstration

    A = [[random.randint(-1, 1) for _ in range(n)] for _ in range(n)]
    M = [[sum(A[i][j] * A[k][l] for i in range(n) for j in range(n)) for k in range(n)] for l in range(n)]

    M_d = [[M[i][j] ** d if i == j else 0 for j in range(n)] for i in range(n)]
    norm = spectral_norm(M_d)
    lower_bound = communication_complexity_lower_bound(n, Fraction(1, 2))

    ratio = norm / lower_bound
    conjecture_holds = ratio >= c

    return {
        "metric_name": "Spectral Norm Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} < {c}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")